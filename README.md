# Python Pac-Man: A Custom Clone
This is a Pac-Man clone developed from scratch in Python, using the Pygame library. It features a custom-built, image-seeded randomness engine for ghost behavior and includes multiple, selectable levels.

## Features
- **Multiple** Custom Maps: Choose from several unique, custom-designed maps from the main menu, each with different layouts and sizes.

- **Image-Seeded Randomness**: Ghost AI is powered by a unique randomness engine. The starting seed is generated from a provided image, making their behavior unpredictable.

- **Classic Gameplay Loop**: Features a complete gameplay experience with dot collection, scoring, a life system, and a "Game Over" state.

- **Dynamic Ghost AI**: Ghosts don't just follow set paths; they make random decisions at every intersection, making each session a new challenge.

- **Modular Codebase**: The project is cleanly organized into modules for the player, ghosts, maze, maps, and configuration, making it easy to understand and extend.

## Project Structure
The project is organized into logical modules for easy management:

PACMAN/

├── 🎨 assets/             # Contains all game assets (images, sounds, fonts)

├── ⚙️ config.py           # Game configuration and global constants (colors, speed, etc.)

├── 🚀 main.py             # Main game entry point, menu, and game loop handler

├── 🗺️ maps.py             # All map layouts and character spawn points

├── 🟡 player.py           # The Player class, handling movement and input

├── 👻 ghost.py            # The Ghost class, handling AI and movement

├── 🎲 motor_aleatorio.py  # The custom image-based randomness engine

└── 📝 requirements.txt    # Project dependencies

Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

## Prerequisites
Python 3.8 or newer


pip (Python package installer)

## Installation
Clone the repository:

Bash

```sh
git clone https://github.com/your-username/pacman-project.git
cd pacman-project
Create and activate a virtual environment:

On Windows:

Bash

python -m venv venv
.\venv\Scripts\Activate.ps1

On macOS / Linux:

Bash

python3 -m venv venv
source venv/bin/activate
Install the dependencies:
The requirements.txt file lists all necessary libraries. Install them with:

Bash

pip install -r requirements.txt
How to Play 🎮
Run the game:
Make sure your virtual environment is active, then run:

Bash

python main.py

```

## Navigate the Menu:

Use the UP and DOWN arrow keys to select a map.

Press ENTER to start playing.

## Gameplay:

Use the ARROW KEYS to control Pac-Man's movement.

Your goal is to eat all the white dots in the maze while avoiding the ghosts.

If a ghost touches you, you lose a life and restart at the beginning.

Press ESC at any time during the game to return to the main menu.