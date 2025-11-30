"""
Main entry point for the Music Player application.

This script initializes the Player_Window class from the player module
and starts the music player UI. The application relies on the following
modules in the project:

- audio.py       : Handles audio playback and logic
- buttons.py     : Implements interactive UI buttons
- slider.py      : Manages volume and progress sliders
- settings.py    : Stores application settings
- Images/        : Contains all UI-related images

Usage:
    Run this script directly to launch the music player.

Example:
    $ python main.py
"""

from player import Player_Window

def main():
    """
    Create and start the Vibe music player.

    Initializes a Player_Window object and calls its start_player() method
    to launch the music player interface and handle playback.
    """

    music_player = Player_Window()
    music_player.start_player()

if __name__ == "__main__":
    main()
