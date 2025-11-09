#!/usr/bin/env python3
"""
Two-Player Dancing Mice Game
A fun pygame where two mice can dance together!

Controls:
Player 1 (Blue Mouse):
  - WASD: Move
  - Q: Spin dance
  - E: Jump dance

Player 2 (Pink Mouse):
  - Arrow Keys: Move
  - < (Left Shift): Spin dance
  - > (Right Shift): Jump dance

ESC: Quit
"""

import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
PINK = (255, 150, 200)
PURPLE = (200, 100, 255)
YELLOW = (255, 255, 100)
GRAY = (200, 200, 200)

class DancingMouse:
    def __init__(self, x, y, color, name, controls):
        self.x = x
        self.y = y
        self.base_color = color
        self.name = name
        self.controls = controls
        self.size = 30
        self.speed = 5

        # Dance state
        self.is_spinning = False
        self.is_jumping = False
        self.spin_angle = 0
        self.jump_offset = 0
        self.jump_velocity = 0

        # Trail effect
        self.trail = []
        self.max_trail_length = 15

        # Animation
        self.bounce_offset = 0
        self.bounce_direction = 1

    def handle_input(self, keys):
        """Handle player input for movement and dancing"""
        # Movement
        if keys[self.controls['up']]:
            self.y -= self.speed
        if keys[self.controls['down']]:
            self.y += self.speed
        if keys[self.controls['left']]:
            self.x -= self.speed
        if keys[self.controls['right']]:
            self.x += self.speed

        # Dance moves
        if keys[self.controls['dance1']]:
            self.is_spinning = True
        else:
            self.is_spinning = False
            self.spin_angle = 0

        if keys[self.controls['dance2']]:
            if not self.is_jumping and self.jump_offset == 0:
                self.is_jumping = True
                self.jump_velocity = -15

        # Keep mouse on screen
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))

    def update(self):
        """Update mouse animation and effects"""
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        # Update spin animation
        if self.is_spinning:
            self.spin_angle += 20
            if self.spin_angle >= 360:
                self.spin_angle = 0

        # Update jump animation
        if self.is_jumping or self.jump_offset != 0:
            self.jump_velocity += 1  # Gravity
            self.jump_offset += self.jump_velocity

            if self.jump_offset >= 0:
                self.jump_offset = 0
                self.jump_velocity = 0
                self.is_jumping = False

        # Idle bounce animation
        if not self.is_spinning and not self.is_jumping:
            self.bounce_offset += 0.15 * self.bounce_direction
            if abs(self.bounce_offset) > 3:
                self.bounce_direction *= -1

    def draw(self, screen):
        """Draw the mouse with animations"""
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            trail_size = self.size * (i / len(self.trail)) * 0.5
            color = tuple(min(255, c + 50) for c in self.base_color)
            pygame.draw.circle(screen, color, (int(tx), int(ty)), int(trail_size))

        # Calculate position with animations
        draw_y = int(self.y + self.jump_offset + self.bounce_offset)

        # Draw shadow (if not jumping high)
        if self.jump_offset > -20:
            shadow_alpha = max(50, 150 + self.jump_offset * 3)
            shadow_size = self.size + abs(self.jump_offset) * 0.3
            shadow_surface = pygame.Surface((shadow_size * 2, shadow_size * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (*GRAY, int(shadow_alpha)),
                              shadow_surface.get_rect())
            screen.blit(shadow_surface,
                       (self.x - shadow_size, self.y - shadow_size // 4))

        # Mouse body (larger circle)
        body_color = self.base_color
        if self.is_spinning:
            # Rainbow effect while spinning
            hue = (self.spin_angle + pygame.time.get_ticks() / 10) % 360
            body_color = self._hsv_to_rgb(hue, 0.7, 1.0)

        pygame.draw.circle(screen, body_color, (int(self.x), draw_y), self.size)
        pygame.draw.circle(screen, BLACK, (int(self.x), draw_y), self.size, 2)

        # Calculate ear positions with spin
        spin_rad = math.radians(self.spin_angle)

        # Left ear
        left_ear_x = self.x - self.size * 0.5 * math.cos(spin_rad) - self.size * 0.3 * math.sin(spin_rad)
        left_ear_y = draw_y - self.size * 0.7 * math.cos(spin_rad) + self.size * 0.3 * math.sin(spin_rad)
        pygame.draw.circle(screen, body_color, (int(left_ear_x), int(left_ear_y)), self.size // 2)
        pygame.draw.circle(screen, BLACK, (int(left_ear_x), int(left_ear_y)), self.size // 2, 2)
        pygame.draw.circle(screen, PINK, (int(left_ear_x), int(left_ear_y)), self.size // 3)

        # Right ear
        right_ear_x = self.x + self.size * 0.5 * math.cos(spin_rad) - self.size * 0.3 * math.sin(spin_rad)
        right_ear_y = draw_y - self.size * 0.7 * math.cos(spin_rad) - self.size * 0.3 * math.sin(spin_rad)
        pygame.draw.circle(screen, body_color, (int(right_ear_x), int(right_ear_y)), self.size // 2)
        pygame.draw.circle(screen, BLACK, (int(right_ear_x), int(right_ear_y)), self.size // 2, 2)
        pygame.draw.circle(screen, PINK, (int(right_ear_x), int(right_ear_y)), self.size // 3)

        # Eyes
        eye_offset_x = 10
        eye_offset_y = -5

        # Left eye
        left_eye_x = self.x - eye_offset_x
        left_eye_y = draw_y + eye_offset_y
        pygame.draw.circle(screen, BLACK, (int(left_eye_x), int(left_eye_y)), 4)

        # Right eye
        right_eye_x = self.x + eye_offset_x
        right_eye_y = draw_y + eye_offset_y
        pygame.draw.circle(screen, BLACK, (int(right_eye_x), int(right_eye_y)), 4)

        # Nose
        nose_x = self.x
        nose_y = draw_y + 5
        pygame.draw.circle(screen, (255, 150, 150), (int(nose_x), int(nose_y)), 3)

        # Whiskers
        whisker_color = BLACK
        whisker_length = 20
        # Left whiskers
        pygame.draw.line(screen, whisker_color,
                        (int(self.x - 15), int(draw_y)),
                        (int(self.x - 15 - whisker_length), int(draw_y - 5)), 1)
        pygame.draw.line(screen, whisker_color,
                        (int(self.x - 15), int(draw_y)),
                        (int(self.x - 15 - whisker_length), int(draw_y + 5)), 1)
        # Right whiskers
        pygame.draw.line(screen, whisker_color,
                        (int(self.x + 15), int(draw_y)),
                        (int(self.x + 15 + whisker_length), int(draw_y - 5)), 1)
        pygame.draw.line(screen, whisker_color,
                        (int(self.x + 15), int(draw_y)),
                        (int(self.x + 15 + whisker_length), int(draw_y + 5)), 1)

        # Draw dance particles if dancing
        if self.is_spinning or self.is_jumping:
            self._draw_dance_particles(screen)

    def _draw_dance_particles(self, screen):
        """Draw sparkle particles around dancing mouse"""
        for i in range(5):
            angle = random.random() * math.pi * 2
            distance = self.size + random.randint(10, 30)
            px = self.x + math.cos(angle) * distance
            py = self.y + math.sin(angle) * distance
            particle_size = random.randint(2, 5)
            particle_color = random.choice([YELLOW, WHITE, PURPLE, self.base_color])
            pygame.draw.circle(screen, particle_color, (int(px), int(py)), particle_size)

    def _hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dancing Mice - Two Player Dance Party!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Create players
        player1_controls = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'dance1': pygame.K_q,
            'dance2': pygame.K_e
        }

        player2_controls = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'dance1': pygame.K_RSHIFT,
            'dance2': pygame.K_LSHIFT
        }

        self.player1 = DancingMouse(250, 350, BLUE, "Blue Mouse", player1_controls)
        self.player2 = DancingMouse(750, 350, PINK, "Pink Mouse", player2_controls)

        # Background stars
        self.stars = []
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'twinkle': random.random()
            })

    def draw_background(self):
        """Draw animated background"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(20 + 30 * color_ratio)
            g = int(20 + 50 * color_ratio)
            b = int(50 + 80 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Twinkling stars
        for star in self.stars:
            star['twinkle'] += 0.1
            brightness = abs(math.sin(star['twinkle'])) * 255
            color = (int(brightness), int(brightness), int(brightness))
            pygame.draw.circle(self.screen, color, (star['x'], star['y']), star['size'])

    def draw_ui(self):
        """Draw UI elements"""
        # Title
        title = self.font.render("Dancing Mice Dance Party!", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))

        # Add shadow
        shadow = self.font.render("Dancing Mice Dance Party!", True, BLACK)
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 2, 32))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        # Player 1 controls
        p1_text = self.small_font.render("Player 1 (Blue): WASD-move | Q-spin | E-jump", True, BLUE)
        self.screen.blit(p1_text, (10, SCREEN_HEIGHT - 60))

        # Player 2 controls
        p2_text = self.small_font.render("Player 2 (Pink): Arrows-move | RShift-spin | LShift-jump", True, PINK)
        self.screen.blit(p2_text, (10, SCREEN_HEIGHT - 30))

        # Exit hint
        exit_text = self.small_font.render("ESC to quit", True, WHITE)
        self.screen.blit(exit_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30))

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

            # Get pressed keys
            keys = pygame.key.get_pressed()

            # Update
            self.player1.handle_input(keys)
            self.player2.handle_input(keys)
            self.player1.update()
            self.player2.update()

            # Draw
            self.draw_background()
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
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
