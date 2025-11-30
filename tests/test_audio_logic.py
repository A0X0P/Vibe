"""Unit tests for AudioPlayer logic."""
from unittest.mock import patch, MagicMock
import pygame

# Mock pygame.mixer before importing
pygame.mixer = MagicMock()




class TestAudioPlayerInitialization:
    """Test AudioPlayer initialization."""
    
    def test_initialization_default_values(self, audio_player):
        """Test that AudioPlayer initializes with correct default values."""
        assert audio_player.playlist == []
        assert audio_player.index == 0
        assert audio_player.is_playing is False
        assert audio_player.paused is False
        assert audio_player.loop_mode == 0
        assert audio_player.song_length == 0
        assert audio_player.seek_offset == 0
        assert audio_player.current_song_position == "0:00"
        assert audio_player.current_song_length == "0:00"


class TestTimeConversion:
    """Test time conversion utilities."""
    
    def test_convert_sec_min_zero_seconds(self, audio_player):
        """Test time conversion for 0 seconds."""
        assert audio_player.convert_sec_min(0) == "0:00"
    
    def test_convert_sec_min_one_minute(self, audio_player):
        """Test time conversion for exactly 1 minute."""
        assert audio_player.convert_sec_min(60) == "1:00"
    
    def test_convert_sec_min_with_seconds(self, audio_player):
        """Test time conversion with minutes and seconds."""
        assert audio_player.convert_sec_min(65) == "1:05"
        assert audio_player.convert_sec_min(125) == "2:05"
        assert audio_player.convert_sec_min(3661) == "61:01"
    
    def test_convert_sec_min_handles_floats(self, audio_player):
        """Test time conversion with float input."""
        assert audio_player.convert_sec_min(65.7) == "1:05"
        assert audio_player.convert_sec_min(89.9) == "1:29"


class TestLoopMode:
    """Test loop mode cycling."""
    
    def test_toggle_loop_mode_cycles_correctly(self, audio_player):
        """Test that loop mode cycles through all states."""
        assert audio_player.loop_mode == 0
        
        # Off -> Loop All
        mode = audio_player.toggle_loop_mode()
        assert mode == 1
        assert audio_player.loop_mode == 1
        
        # Loop All -> Loop One
        mode = audio_player.toggle_loop_mode()
        assert mode == 2
        assert audio_player.loop_mode == 2
        
        # Loop One -> Off (cycles back)
        mode = audio_player.toggle_loop_mode()
        assert mode == 0
        assert audio_player.loop_mode == 0
    
    def test_toggle_loop_mode_multiple_cycles(self, audio_player):
        """Test that loop mode continues cycling correctly."""
        for _ in range(10):
            audio_player.toggle_loop_mode()
        
        # After 10 toggles, should be back at mode 1 because (10 % 3 = 1)
        assert audio_player.loop_mode == 1


class TestPositionTracking:
    """Test playback position tracking."""
    
    def test_get_current_position_no_playlist(self, audio_player):
        """Test position returns 0 when no song is loaded."""
        assert audio_player.get_current_position() == 0
    
    def test_get_current_position_when_paused(self, audio_player_with_playlist):
        """Test position returns seek_offset when paused."""
        audio_player_with_playlist.paused = True
        audio_player_with_playlist.seek_offset = 45.5
        
        assert audio_player_with_playlist.get_current_position() == 45.5
    
    @patch('pygame.time.get_ticks')
    def test_get_current_position_during_playback(self, mock_ticks, audio_player_with_playlist):
        """Test position calculation during playback."""
        audio_player_with_playlist.is_playing = True
        audio_player_with_playlist.paused = False
        audio_player_with_playlist.seek_offset = 10.0
        audio_player_with_playlist.last_update_time = 1000
        
        # Simulate 5 seconds elapsed
        mock_ticks.return_value = 6000
        
        position = audio_player_with_playlist.get_current_position()
        assert position == 15.0  
    
    @patch('pygame.time.get_ticks')
    def test_get_current_position_does_not_exceed_song_length(self, mock_ticks, audio_player_with_playlist):
        """Test position is capped at song length."""
        audio_player_with_playlist.is_playing = True
        audio_player_with_playlist.paused = False
        audio_player_with_playlist.seek_offset = 175.0
        audio_player_with_playlist.last_update_time = 1000
        
        # Simulate 10 seconds elapsed 
        mock_ticks.return_value = 11000
        
        position = audio_player_with_playlist.get_current_position()
        assert position == 180  # Capped at song length
    
    def test_update_current_position_no_playlist(self, audio_player):
        """Test position string is 0:00 when no playlist."""
        audio_player.update_current_position()
        assert audio_player.current_song_position == "0:00"
    
    @patch('pygame.time.get_ticks')
    def test_update_current_position_with_song(self, mock_ticks, audio_player_with_playlist):
        """Test position string updates correctly."""
        audio_player_with_playlist.is_playing = True
        audio_player_with_playlist.seek_offset = 65.0
        audio_player_with_playlist.last_update_time = 1000
        mock_ticks.return_value = 1000
        
        audio_player_with_playlist.update_current_position()
        assert audio_player_with_playlist.current_song_position == "1:05"


class TestSongSeeking:
    """Test song seeking functionality."""
    
    def test_adjust_song_no_playlist_does_nothing(self, audio_player):
        """Test adjust_song doesn't crash with empty playlist."""
        # No need to mock - just verify no crash
        audio_player.adjust_song(0.5)
        # If we get here without exception, test passes
        assert True
    
    @patch('audio.pygame.mixer.music.set_pos')
    @patch('audio.pygame.time.get_ticks')
    def test_adjust_song_sets_position_correctly(self, mock_ticks, mock_set_pos, audio_player_with_playlist):
        """Test adjust_song calculates and sets correct position."""
        mock_ticks.return_value = 5000
        
        # Seek to 50% (90 seconds)
        audio_player_with_playlist.adjust_song(0.5)
        
        mock_set_pos.assert_called_once_with(90.0)
        assert audio_player_with_playlist.seek_offset == 90.0
        assert audio_player_with_playlist.last_update_time == 5000
    
    @patch('audio.pygame.mixer.music.set_pos')
    @patch('audio.pygame.time.get_ticks')
    def test_adjust_song_to_beginning(self, mock_ticks, mock_set_pos, audio_player_with_playlist):
        """Test seeking to the beginning (0%)."""
        mock_ticks.return_value = 5000
        
        audio_player_with_playlist.adjust_song(0.0)
        
        mock_set_pos.assert_called_once_with(0.0)
        assert audio_player_with_playlist.seek_offset == 0.0
    
    @patch('audio.pygame.mixer.music.set_pos')
    @patch('audio.pygame.time.get_ticks')
    def test_adjust_song_to_end(self, mock_ticks, mock_set_pos, audio_player_with_playlist):
        """Test seeking near the end (100%)."""
        mock_ticks.return_value = 5000
        
        audio_player_with_playlist.adjust_song(1.0)
        
        mock_set_pos.assert_called_once_with(180.0)
        assert audio_player_with_playlist.seek_offset == 180.0


class TestPlaylistNavigation:
    """Test playlist navigation logic."""
    
    @patch('audio.pygame.mixer.music.load')
    @patch('audio.pygame.mixer.music.play')
    @patch('audio.pygame.time.get_ticks')
    def test_next_song_advances_index(self, mock_ticks, mock_play, mock_load, audio_player_with_playlist):
        """Test next_song advances to next track."""
        mock_ticks.return_value = 1000
        audio_player_with_playlist.index = 0
        
        audio_player_with_playlist.next_song()
        
        assert audio_player_with_playlist.index == 1
        mock_load.assert_called_with("song2.mp3")
    
    @patch('audio.pygame.mixer.music.load')
    @patch('audio.pygame.mixer.music.play')
    @patch('audio.pygame.time.get_ticks')
    def test_next_song_wraps_to_beginning(self, mock_ticks, mock_play, mock_load, audio_player_with_playlist):
        """Test next_song wraps to first track at end."""
        mock_ticks.return_value = 1000
        audio_player_with_playlist.index = 2  # Last song
        
        audio_player_with_playlist.next_song()
        
        assert audio_player_with_playlist.index == 0
        mock_load.assert_called_with("song1.mp3")
    
    @patch('audio.pygame.mixer.music.load')
    @patch('audio.pygame.mixer.music.play')
    @patch('audio.pygame.time.get_ticks')
    def test_previous_song_goes_back(self, mock_ticks, mock_play, mock_load, audio_player_with_playlist):
        """Test previous_song goes to previous track."""
        mock_ticks.return_value = 1000
        audio_player_with_playlist.index = 1
        
        audio_player_with_playlist.previous_song()
        
        assert audio_player_with_playlist.index == 0
        mock_load.assert_called_with("song1.mp3")
    
    @patch('audio.pygame.mixer.music.load')
    @patch('audio.pygame.mixer.music.play')
    @patch('audio.pygame.time.get_ticks')
    def test_previous_song_wraps_to_end(self, mock_ticks, mock_play, mock_load, audio_player_with_playlist):
        """Test previous_song wraps to last track at beginning."""
        mock_ticks.return_value = 1000
        audio_player_with_playlist.index = 0  # First song
        
        audio_player_with_playlist.previous_song()
        
        assert audio_player_with_playlist.index == 2
        mock_load.assert_called_with("song3.mp3")
    
    def test_next_song_empty_playlist_does_nothing(self, audio_player):
        """Test next_song with empty playlist doesn't crash."""
        audio_player.next_song()
        assert audio_player.index == 0
    
    def test_previous_song_empty_playlist_does_nothing(self, audio_player):
        """Test previous_song with empty playlist doesn't crash."""
        audio_player.previous_song()
        assert audio_player.index == 0


class TestTogglePlayPause:
    """Test play/pause toggle functionality."""
    
    def test_toggle_play_pause_empty_playlist_does_nothing(self, audio_player):
        """Test toggle with empty playlist doesn't crash."""
        audio_player.toggle_play_pause()
        assert audio_player.is_playing is False
    
    @patch('audio.pygame.mixer.music.load')
    @patch('audio.pygame.mixer.music.play')
    @patch('audio.pygame.time.get_ticks')
    def test_toggle_play_pause_starts_playback(self, mock_ticks, mock_play, mock_load, audio_player_with_playlist):
        """Test toggle starts playback when stopped."""
        mock_ticks.return_value = 1000
        audio_player_with_playlist.is_playing = False
        
        audio_player_with_playlist.toggle_play_pause()
        
        assert audio_player_with_playlist.is_playing is True
        mock_load.assert_called_once()
    
    @patch('audio.pygame.mixer.music.pause')
    def test_toggle_play_pause_pauses_playback(self, mock_pause, audio_player_with_playlist):
        """Test toggle pauses when playing."""
        audio_player_with_playlist.is_playing = True
        
        audio_player_with_playlist.toggle_play_pause()
        
        assert audio_player_with_playlist.is_playing is False
        mock_pause.assert_called_once()