"""Shared pytest fixtures for all tests."""
from unittest.mock import Mock, MagicMock
import pytest
import pygame

# Mock pygame.mixer globally for all tests
pygame.mixer = MagicMock()


@pytest.fixture
def mock_player_window():
    """Create a mock player window for testing AudioPlayer."""
    mock_window = Mock()
    mock_window.root = Mock()
    mock_window.pause_bnt = Mock()
    mock_window.play_bnt = Mock()
    mock_window.current_icon = Mock()
    return mock_window


@pytest.fixture
def audio_player(mock_player_window):
    """Create an AudioPlayer instance with mocked dependencies."""
    from unittest.mock import patch
    
    with patch('pygame.mixer.init'):
        with patch('pygame.mixer.music.set_endevent'):
            from audio import AudioPlayer
            player = AudioPlayer(mock_player_window)
            return player


@pytest.fixture
def audio_player_with_playlist(mock_player_window):
    """Create audio player with a pre-loaded playlist."""
    from unittest.mock import patch
    
    with patch('pygame.mixer.init'):
        with patch('pygame.mixer.music.set_endevent'):
            from audio import AudioPlayer
            player = AudioPlayer(mock_player_window)
            player.playlist = ["song1.mp3", "song2.mp3", "song3.mp3"]
            player.song_length = 180
            player.AUDIO_OK = True
            return player