#!/usr/bin/env python3
"""
Mouse Cave Adventure - Two Player Game
A story-driven 2D platformer where a poor mouse must navigate through a dangerous
cave to reach a rich mouse's mansion!

Story:
- Rich Mouse (Player 1): Lives in a luxurious mansion with piles of gold
- Poor Mouse (Player 2): Must brave the dangerous cave to reach the mansion

Controls:
Player 1 (Rich Mouse - Gold):
  - WASD: Move and jump
  - Q: Bite (when near other mouse)

Player 2 (Poor Mouse - Gray):
  - Arrow Keys: Move and jump
  - Right Shift: Bite (when near other mouse)

ESC: Quit
R: Reset game
"""

import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLUE = (100, 149, 237)
PURPLE = (147, 112, 219)
YELLOW = (255, 255, 0)

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5

class Mouse:
    def __init__(self, x, y, color, name, controls, is_rich=False):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.base_color = color
        self.name = name
        self.controls = controls
        self.is_rich = is_rich

        self.width = 30
        self.height = 30
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True

        # Game state
        self.money = 1000 if is_rich else 10
        self.health = 3
        self.is_crying = False
        self.cry_timer = 0
        self.is_biting = False
        self.bite_timer = 0
        self.bite_cooldown = 0

        # Animation
        self.bounce_offset = 0
        self.walk_cycle = 0

    def handle_input(self, keys, platforms):
        """Handle player input"""
        # Horizontal movement
        self.vel_x = 0
        if keys[self.controls['left']]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False
            self.walk_cycle += 0.3
        if keys[self.controls['right']]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True
            self.walk_cycle += 0.3

        # Jumping
        if keys[self.controls['jump']] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

        # Biting
        if keys[self.controls['bite']] and self.bite_cooldown <= 0:
            self.is_biting = True
            self.bite_timer = 20
            self.bite_cooldown = 60

    def update(self, platforms, hazards):
        """Update mouse physics and state"""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY

        # Limit fall speed
        self.vel_y = min(self.vel_y, 20)

        # Move horizontally
        self.x += self.vel_x

        # Check horizontal collisions
        mouse_rect = pygame.Rect(self.x - self.width//2, self.y - self.height,
                                 self.width, self.height)
        for platform in platforms:
            if mouse_rect.colliderect(platform):
                if self.vel_x > 0:  # Moving right
                    self.x = platform.left - self.width//2
                elif self.vel_x < 0:  # Moving left
                    self.x = platform.right + self.width//2
                self.vel_x = 0

        # Move vertically
        self.y += self.vel_y

        # Check vertical collisions
        self.on_ground = False
        mouse_rect = pygame.Rect(self.x - self.width//2, self.y - self.height,
                                 self.width, self.height)
        for platform in platforms:
            if mouse_rect.colliderect(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping up
                    self.y = platform.bottom + self.height
                    self.vel_y = 0

        # Check hazard collisions
        for hazard in hazards:
            if mouse_rect.colliderect(hazard['rect']):
                if hazard['type'] == 'spike':
                    self.take_damage()
                    self.respawn()

        # Update timers
        if self.cry_timer > 0:
            self.cry_timer -= 1
            if self.cry_timer == 0:
                self.is_crying = False

        if self.bite_timer > 0:
            self.bite_timer -= 1
            if self.bite_timer == 0:
                self.is_biting = False

        if self.bite_cooldown > 0:
            self.bite_cooldown -= 1

        # Bounce animation when standing
        if self.on_ground and self.vel_x == 0:
            self.bounce_offset = math.sin(pygame.time.get_ticks() / 300) * 2
        else:
            self.bounce_offset = 0

        # Keep in bounds
        self.x = max(15, min(SCREEN_WIDTH - 15, self.x))

        # Fall off bottom = death
        if self.y > SCREEN_HEIGHT + 50:
            self.take_damage()
            self.respawn()

    def take_damage(self):
        """Take damage and start crying"""
        self.health -= 1
        self.is_crying = True
        self.cry_timer = 120

    def respawn(self):
        """Respawn at starting position"""
        self.x = self.start_x
        self.y = self.start_y
        self.vel_x = 0
        self.vel_y = 0

    def collect_money(self, amount):
        """Collect money"""
        self.money += amount

    def can_bite(self, other_mouse):
        """Check if this mouse can bite another mouse"""
        if not self.is_biting:
            return False
        distance = math.sqrt((self.x - other_mouse.x)**2 + (self.y - other_mouse.y)**2)
        return distance < 50

    def draw(self, screen, camera_x=0):
        """Draw the mouse with all its features"""
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y + self.bounce_offset)

        # Draw shadow
        shadow_surface = pygame.Surface((self.width + 10, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (*BLACK, 100), shadow_surface.get_rect())
        screen.blit(shadow_surface, (draw_x - (self.width + 10)//2, draw_y - 5))

        # Body color (changes when crying or biting)
        body_color = self.base_color
        if self.is_crying:
            body_color = tuple(min(255, c + 30) for c in self.base_color)

        # Draw body
        body_rect = pygame.Rect(draw_x - self.width//2, draw_y - self.height,
                               self.width, self.height)
        pygame.draw.ellipse(screen, body_color, body_rect)
        pygame.draw.ellipse(screen, BLACK, body_rect, 2)

        # Draw ears
        ear_offset = 1 if not self.facing_right else -1
        left_ear = (draw_x - 12 + ear_offset, draw_y - self.height - 8)
        right_ear = (draw_x + 12 + ear_offset, draw_y - self.height - 8)

        pygame.draw.circle(screen, body_color, left_ear, 8)
        pygame.draw.circle(screen, BLACK, left_ear, 8, 2)
        pygame.draw.circle(screen, (255, 182, 193), left_ear, 5)

        pygame.draw.circle(screen, body_color, right_ear, 8)
        pygame.draw.circle(screen, BLACK, right_ear, 8, 2)
        pygame.draw.circle(screen, (255, 182, 193), right_ear, 5)

        # Draw eyes
        eye_x_offset = 8 if self.facing_right else -8
        eye_y = draw_y - self.height + 10

        # Crying eyes
        if self.is_crying:
            # Closed crying eyes
            pygame.draw.arc(screen, BLACK,
                          (draw_x + eye_x_offset - 3, eye_y - 3, 6, 6),
                          0, math.pi, 2)
            # Tears
            tear_y = eye_y + 5
            for i in range(3):
                tear_pos = tear_y + i * 8 + (self.cry_timer % 20)
                if tear_pos < draw_y:
                    pygame.draw.circle(screen, BLUE,
                                     (draw_x + eye_x_offset, int(tear_pos)), 2)
        else:
            # Normal eyes
            pygame.draw.circle(screen, BLACK, (draw_x + eye_x_offset, eye_y), 4)
            pygame.draw.circle(screen, WHITE, (draw_x + eye_x_offset + 1, eye_y - 1), 2)

        # Draw nose
        nose_x = draw_x + (12 if self.facing_right else -12)
        nose_y = draw_y - self.height + 18
        pygame.draw.circle(screen, (255, 105, 180), (nose_x, nose_y), 3)

        # Draw whiskers
        whisker_length = 15
        whisker_y1 = draw_y - self.height + 15
        whisker_y2 = draw_y - self.height + 20

        if self.facing_right:
            # Right whiskers
            pygame.draw.line(screen, BLACK, (draw_x + 10, whisker_y1),
                           (draw_x + 10 + whisker_length, whisker_y1 - 3), 1)
            pygame.draw.line(screen, BLACK, (draw_x + 10, whisker_y2),
                           (draw_x + 10 + whisker_length, whisker_y2 + 3), 1)
        else:
            # Left whiskers
            pygame.draw.line(screen, BLACK, (draw_x - 10, whisker_y1),
                           (draw_x - 10 - whisker_length, whisker_y1 - 3), 1)
            pygame.draw.line(screen, BLACK, (draw_x - 10, whisker_y2),
                           (draw_x - 10 - whisker_length, whisker_y2 + 3), 1)

        # Draw tail
        tail_start_x = draw_x + (-8 if self.facing_right else 8)
        tail_start_y = draw_y - 10
        tail_wave = math.sin(pygame.time.get_ticks() / 200) * 10

        tail_points = [
            (tail_start_x, tail_start_y),
            (tail_start_x + (-15 if self.facing_right else 15), tail_start_y + 5 + tail_wave),
            (tail_start_x + (-25 if self.facing_right else 25), tail_start_y + 15)
        ]
        pygame.draw.lines(screen, body_color, False, tail_points, 4)
        pygame.draw.lines(screen, BLACK, False, tail_points, 1)

        # Biting animation
        if self.is_biting:
            bite_x = draw_x + (25 if self.facing_right else -25)
            bite_y = draw_y - self.height + 15
            # Draw "BITE!" text
            font = pygame.font.Font(None, 20)
            bite_text = font.render("BITE!", True, RED)
            screen.blit(bite_text, (bite_x - 15, bite_y - 20))
            # Draw bite effect
            for i in range(3):
                angle = (self.bite_timer * 30 + i * 120) % 360
                rad = math.radians(angle)
                effect_x = bite_x + math.cos(rad) * 15
                effect_y = bite_y + math.sin(rad) * 15
                pygame.draw.circle(screen, RED, (int(effect_x), int(effect_y)), 3)

        # Draw crown for rich mouse
        if self.is_rich:
            crown_y = draw_y - self.height - 15
            crown_points = [
                (draw_x - 10, crown_y),
                (draw_x - 8, crown_y - 8),
                (draw_x - 3, crown_y - 3),
                (draw_x, crown_y - 10),
                (draw_x + 3, crown_y - 3),
                (draw_x + 8, crown_y - 8),
                (draw_x + 10, crown_y),
            ]
            pygame.draw.polygon(screen, GOLD, crown_points)
            pygame.draw.polygon(screen, DARK_GOLD, crown_points, 2)
            # Jewels on crown
            pygame.draw.circle(screen, RED, (draw_x, crown_y - 8), 2)


class Coin:
    def __init__(self, x, y, value=10):
        self.x = x
        self.y = y
        self.value = value
        self.collected = False
        self.spin = 0

    def update(self):
        self.spin = (self.spin + 5) % 360

    def draw(self, screen, camera_x=0):
        if self.collected:
            return
        draw_x = int(self.x - camera_x)
        # Spinning coin effect
        width = abs(math.sin(math.radians(self.spin)) * 15)
        coin_rect = pygame.Rect(draw_x - width/2, self.y - 15, max(3, width), 20)
        pygame.draw.ellipse(screen, GOLD, coin_rect)
        pygame.draw.ellipse(screen, DARK_GOLD, coin_rect, 2)

    def check_collision(self, mouse):
        if self.collected:
            return False
        distance = math.sqrt((self.x - mouse.x)**2 + (self.y - mouse.y)**2)
        if distance < 30:
            self.collected = True
            return True
        return False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mouse Cave Adventure - Rich vs Poor")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)

        # Camera
        self.camera_x = 0

        # Create players
        player1_controls = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'jump': pygame.K_w,
            'bite': pygame.K_q
        }

        player2_controls = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_UP,
            'bite': pygame.K_RSHIFT
        }

        self.rich_mouse = Mouse(1000, 200, GOLD, "Rich Mouse", player1_controls, is_rich=True)
        self.poor_mouse = Mouse(100, 500, GRAY, "Poor Mouse", player2_controls, is_rich=False)

        # World elements
        self.platforms = []
        self.hazards = []
        self.coins = []
        self.build_world()

    def build_world(self):
        """Build the game world with cave and mansion"""
        # Ground
        self.platforms.append(pygame.Rect(0, 650, 500, 50))  # Cave entrance
        self.platforms.append(pygame.Rect(0, 550, 150, 20))  # Cave platform 1
        self.platforms.append(pygame.Rect(200, 500, 150, 20))  # Cave platform 2
        self.platforms.append(pygame.Rect(400, 450, 150, 20))  # Cave platform 3
        self.platforms.append(pygame.Rect(600, 400, 150, 20))  # Cave platform 4
        self.platforms.append(pygame.Rect(800, 350, 200, 20))  # Transition
        self.platforms.append(pygame.Rect(1050, 300, 150, 20))  # Mansion entrance

        # Mansion floor
        self.platforms.append(pygame.Rect(850, 250, 350, 20))  # Main floor
        self.platforms.append(pygame.Rect(900, 200, 100, 20))  # Upper platform

        # Cave ceiling/walls
        self.platforms.append(pygame.Rect(0, 0, 700, 50))  # Cave ceiling

        # Hazards (spikes in the cave)
        self.hazards.append({'type': 'spike', 'rect': pygame.Rect(250, 630, 40, 20)})
        self.hazards.append({'type': 'spike', 'rect': pygame.Rect(450, 630, 40, 20)})
        self.hazards.append({'type': 'spike', 'rect': pygame.Rect(150, 530, 30, 20)})
        self.hazards.append({'type': 'spike', 'rect': pygame.Rect(350, 480, 30, 20)})

        # Coins scattered around
        # Cave coins (less valuable)
        for i in range(5):
            self.coins.append(Coin(100 + i * 100, 520, value=5))

        # Mansion coins (more valuable)
        for i in range(10):
            x = 900 + (i % 5) * 40
            y = 230 if i < 5 else 180
            self.coins.append(Coin(x, y, value=20))

    def reset_game(self):
        """Reset the game state"""
        self.rich_mouse = Mouse(1000, 200, GOLD, "Rich Mouse",
                               self.rich_mouse.controls, is_rich=True)
        self.poor_mouse = Mouse(100, 500, GRAY, "Poor Mouse",
                               self.poor_mouse.controls, is_rich=False)
        self.coins = []
        self.build_world()

    def update(self, keys):
        """Update game state"""
        # Update mice
        self.rich_mouse.handle_input(keys, self.platforms)
        self.poor_mouse.handle_input(keys, self.platforms)

        self.rich_mouse.update(self.platforms, self.hazards)
        self.poor_mouse.update(self.platforms, self.hazards)

        # Check bite interactions
        if self.rich_mouse.can_bite(self.poor_mouse):
            self.poor_mouse.take_damage()

        if self.poor_mouse.can_bite(self.rich_mouse):
            self.rich_mouse.take_damage()

        # Update and check coin collisions
        for coin in self.coins:
            coin.update()
            if coin.check_collision(self.rich_mouse):
                self.rich_mouse.collect_money(coin.value)
            if coin.check_collision(self.poor_mouse):
                self.poor_mouse.collect_money(coin.value)

        # Camera follows the average position of both mice
        avg_x = (self.rich_mouse.x + self.poor_mouse.x) / 2
        target_camera = avg_x - SCREEN_WIDTH / 2
        self.camera_x = max(0, min(target_camera, 200))  # Limit camera movement

    def draw_background(self):
        """Draw the background with cave and mansion areas"""
        # Cave area (dark)
        cave_gradient = pygame.Surface((700, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            darkness = int(30 + (y / SCREEN_HEIGHT) * 30)
            color = (darkness, darkness, darkness + 20)
            pygame.draw.line(cave_gradient, color, (0, y), (700, y))
        self.screen.blit(cave_gradient, (int(-self.camera_x), 0))

        # Mansion area (bright and golden)
        mansion_gradient = pygame.Surface((SCREEN_WIDTH - 700, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(255 - ratio * 50)
            g = int(240 - ratio * 40)
            b = int(200 - ratio * 50)
            pygame.draw.line(mansion_gradient, (r, g, b), (0, y), (SCREEN_WIDTH - 700, y))
        self.screen.blit(mansion_gradient, (int(700 - self.camera_x), 0))

        # Draw stars in cave
        for i in range(20):
            x = (i * 37 + 10) % 650
            y = (i * 53 + 20) % 300
            brightness = int(abs(math.sin(pygame.time.get_ticks() / 1000 + i)) * 150 + 100)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness + 50),
                             (int(x - self.camera_x), y), 2)

    def draw_world(self):
        """Draw platforms and hazards"""
        # Draw platforms
        for platform in self.platforms:
            draw_rect = platform.copy()
            draw_rect.x -= int(self.camera_x)

            # Different colors for cave vs mansion
            if platform.x < 800:
                color = DARK_BROWN
                border_color = BLACK
            else:
                color = DARK_GOLD
                border_color = GOLD

            pygame.draw.rect(self.screen, color, draw_rect)
            pygame.draw.rect(self.screen, border_color, draw_rect, 2)

        # Draw hazards
        for hazard in self.hazards:
            draw_rect = hazard['rect'].copy()
            draw_rect.x -= int(self.camera_x)

            if hazard['type'] == 'spike':
                # Draw spikes
                num_spikes = draw_rect.width // 10
                for i in range(num_spikes):
                    spike_x = draw_rect.x + i * 10
                    points = [
                        (spike_x, draw_rect.bottom),
                        (spike_x + 5, draw_rect.top),
                        (spike_x + 10, draw_rect.bottom)
                    ]
                    pygame.draw.polygon(self.screen, RED, points)
                    pygame.draw.polygon(self.screen, BLACK, points, 1)

    def draw_mansion(self):
        """Draw the rich mouse's mansion"""
        mansion_x = int(850 - self.camera_x)

        # Main house
        house_rect = pygame.Rect(mansion_x, 100, 300, 150)
        pygame.draw.rect(self.screen, (255, 250, 205), house_rect)
        pygame.draw.rect(self.screen, DARK_GOLD, house_rect, 3)

        # Roof
        roof_points = [
            (mansion_x - 20, 100),
            (mansion_x + 150, 50),
            (mansion_x + 320, 100)
        ]
        pygame.draw.polygon(self.screen, RED, roof_points)
        pygame.draw.polygon(self.screen, DARK_BROWN, roof_points, 3)

        # Windows
        for i in range(3):
            window_x = mansion_x + 30 + i * 90
            window = pygame.Rect(window_x, 120, 50, 50)
            pygame.draw.rect(self.screen, BLUE, window)
            pygame.draw.rect(self.screen, BLACK, window, 2)
            # Window cross
            pygame.draw.line(self.screen, BLACK,
                           (window_x + 25, 120), (window_x + 25, 170), 2)
            pygame.draw.line(self.screen, BLACK,
                           (window_x, 145), (window_x + 50, 145), 2)

        # Door
        door = pygame.Rect(mansion_x + 125, 190, 50, 60)
        pygame.draw.rect(self.screen, BROWN, door)
        pygame.draw.rect(self.screen, BLACK, door, 2)
        pygame.draw.circle(self.screen, GOLD, (mansion_x + 165, 220), 4)

        # Money piles
        for i in range(3):
            pile_x = mansion_x + 50 + i * 80
            for j in range(3):
                coin_y = 245 - j * 8
                pygame.draw.circle(self.screen, GOLD, (pile_x, coin_y), 8)
                pygame.draw.circle(self.screen, DARK_GOLD, (pile_x, coin_y), 8, 2)

    def draw_ui(self):
        """Draw UI elements"""
        # Poor mouse stats (left side)
        poor_bg = pygame.Surface((250, 120), pygame.SRCALPHA)
        pygame.draw.rect(poor_bg, (*BLACK, 180), poor_bg.get_rect(), border_radius=10)
        self.screen.blit(poor_bg, (10, 10))

        poor_name = self.font.render("Poor Mouse", True, GRAY)
        self.screen.blit(poor_name, (20, 20))

        money_text = self.font.render(f"Money: ${self.poor_mouse.money}", True, GOLD)
        self.screen.blit(money_text, (20, 50))

        # Health hearts
        for i in range(self.poor_mouse.health):
            pygame.draw.circle(self.screen, RED, (30 + i * 25, 95), 8)
            pygame.draw.circle(self.screen, RED, (42 + i * 25, 95), 8)
            points = [
                (36 + i * 25, 92),
                (24 + i * 25, 105),
                (36 + i * 25, 112),
                (48 + i * 25, 105)
            ]
            pygame.draw.polygon(self.screen, RED, points)

        # Rich mouse stats (right side)
        rich_bg = pygame.Surface((250, 120), pygame.SRCALPHA)
        pygame.draw.rect(rich_bg, (*BLACK, 180), rich_bg.get_rect(), border_radius=10)
        self.screen.blit(rich_bg, (SCREEN_WIDTH - 260, 10))

        rich_name = self.font.render("Rich Mouse", True, GOLD)
        self.screen.blit(rich_name, (SCREEN_WIDTH - 250, 20))

        money_text = self.font.render(f"Money: ${self.rich_mouse.money}", True, GOLD)
        self.screen.blit(money_text, (SCREEN_WIDTH - 250, 50))

        # Health hearts
        for i in range(self.rich_mouse.health):
            x_base = SCREEN_WIDTH - 240 + i * 25
            pygame.draw.circle(self.screen, RED, (x_base, 95), 8)
            pygame.draw.circle(self.screen, RED, (x_base + 12, 95), 8)
            points = [
                (x_base + 6, 92),
                (x_base - 6, 105),
                (x_base + 6, 112),
                (x_base + 18, 105)
            ]
            pygame.draw.polygon(self.screen, RED, points)

        # Controls reminder (bottom)
        controls_bg = pygame.Surface((SCREEN_WIDTH - 20, 70), pygame.SRCALPHA)
        pygame.draw.rect(controls_bg, (*BLACK, 150), controls_bg.get_rect(), border_radius=10)
        self.screen.blit(controls_bg, (10, SCREEN_HEIGHT - 80))

        p1_controls = self.font.render("P1: WASD-move | W-jump | Q-bite", True, GOLD)
        p2_controls = self.font.render("P2: Arrows-move | UP-jump | RShift-bite", True, GRAY)
        reset_text = self.font.render("R-Reset | ESC-Quit", True, WHITE)

        self.screen.blit(p1_controls, (20, SCREEN_HEIGHT - 70))
        self.screen.blit(p2_controls, (20, SCREEN_HEIGHT - 45))
        self.screen.blit(reset_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 57))

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()

            # Get pressed keys
            keys = pygame.key.get_pressed()

            # Update
            self.update(keys)

            # Draw
            self.draw_background()
            self.draw_world()
            self.draw_mansion()

            # Draw coins
            for coin in self.coins:
                coin.draw(self.screen, self.camera_x)

            # Draw mice
            self.rich_mouse.draw(self.screen, self.camera_x)
            self.poor_mouse.draw(self.screen, self.camera_x)

            # Draw UI
            self.draw_ui()

            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
