# Mouse Games Collection 🐭

Two exciting two-player pygame adventures featuring adorable mice!

## Games Included

### 1. Dancing Mice - Dance Party! 💃🕺
A fun cooperative game where adorable mice dance together in a colorful, animated world!

**Features:**
- Two adorable animated mice with smooth movements
- Multiple dance moves including spinning and jumping
- Colorful particle effects when dancing
- Trail effects that follow the mice
- Beautiful animated background with twinkling stars
- Two-player cooperative gameplay

### 2. Cave Adventure - Rich vs Poor 🏰⛏️
An exciting story-driven 2D platformer with asymmetric gameplay!

**Story:**
- Rich Mouse lives in a luxurious mansion with piles of gold
- Poor Mouse must brave the dangerous cave to reach the mansion
- Both mice can bite each other, causing tears and crying
- Collect coins, avoid hazards, and compete for wealth!

**Features:**
- Full 2D platformer mechanics (jumping, gravity, collision)
- Dangerous cave with spikes and hazards
- Beautiful mansion area with treasure
- Bite mechanics with crying animations
- Money collection system
- Health system with visual hearts
- Smooth camera following both players

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

**Dancing Mice:**
```bash
python dancing_mice.py
```

**Cave Adventure:**
```bash
python cave_adventure.py
```

Or make them executable:
```bash
chmod +x dancing_mice.py cave_adventure.py
./dancing_mice.py
./cave_adventure.py
```

## Controls

### Dancing Mice

**Player 1 (Blue Mouse):**
- W/A/S/D - Move up/left/down/right
- Q - Spin dance (rainbow effect!)
- E - Jump dance

**Player 2 (Pink Mouse):**
- Arrow Keys - Move in four directions
- Right Shift - Spin dance (rainbow effect!)
- Left Shift - Jump dance

**General:**
- ESC - Quit the game

### Cave Adventure

**Player 1 (Rich Mouse - Gold with Crown):**
- W/A/S/D - Move left/right
- W - Jump
- Q - Bite (when near other mouse)

**Player 2 (Poor Mouse - Gray):**
- Arrow Keys - Move left/right
- UP - Jump
- Right Shift - Bite (when near other mouse)

**General:**
- ESC - Quit
- R - Reset game

## Gameplay Tips

### Dancing Mice
- Move around and explore the dance floor
- Try spinning while moving to create beautiful rainbow trails
- Jump at the same time as your friend for synchronized dancing
- Experiment with combining different moves
- Get close to each other and dance together!

### Cave Adventure
- Poor Mouse: Navigate carefully through the cave, avoiding deadly spikes
- Rich Mouse: Defend your mansion and treasure from the intruder
- Collect coins to increase your wealth
- Use bite attacks strategically - they make the other mouse cry!
- Watch your health (hearts) - you only have 3 lives
- Poor Mouse starts with $10, Rich Mouse starts with $1000
- Mansion coins are worth more than cave coins

## Game Features

### Dancing Mice
- **Spin Dance**: Hold the spin button for rainbow color effects
- **Jump Dance**: Bounce into the air with gravity physics
- **Particle Effects**: Colorful sparkles appear while dancing
- **Trail System**: Glowing trail follows your movements
- **Animated Background**: Twinkling stars create a party atmosphere

### Cave Adventure
- **2D Platformer Physics**: Real gravity, jumping, and collision detection
- **Bite Mechanics**: Get close and bite to make the other mouse cry with animated tears
- **Crying Animation**: Bitten mice show tears falling down
- **Hazard System**: Deadly spikes damage and respawn you
- **Money System**: Collect spinning gold coins to get rich
- **Health System**: Three hearts per mouse, lose one when hit by hazards or bites
- **Beautiful Mansion**: Rich mouse's golden palace with windows, doors, and treasure piles
- **Dark Cave**: Dangerous underground area with platforms and obstacles
- **Dynamic Camera**: Follows both players to keep action visible

## Technical Details

- Built with Python and Pygame
- Runs at 60 FPS for smooth animation
- Dancing Mice: 1000x700 pixels
- Cave Adventure: 1200x700 pixels with scrolling camera
- Features custom particle systems, physics engine, and animation states

## Have Fun!

Grab a friend and try both games! Whether you want to dance together or compete for treasure, these mice are ready for adventure! 🎉

---

Made with ❤️ using Pygame
