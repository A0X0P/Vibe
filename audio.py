from tkinter import filedialog
import pygame

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3



class AudioPlayer:
    """
    Manages audio playback using pygame.mixer.music.
    
    This class handles all audio operations including playback control,
    playlist management, volume adjustment, song seeking, loop modes,
    and metadata extraction from MP3 files.
    
    Attributes
    ----------
    player_window : Player_Window
        Reference to the main player window for UI updates
    root : tk.Tk
        Tkinter root window for file dialogs
    pause_bnt : Buttons
        Reference to pause button
    play_bnt : Buttons
        Reference to play button
    current_icon : Buttons
        Currently displayed play/pause icon
    playlist : list[str]
        List of file paths to MP3 files in the playlist
    index : int
        Current position in the playlist (0-indexed)
    is_playing : bool
        True if music is currently playing
    paused : bool
        True if music is paused
    loop_mode : int
        Loop mode (0=off, 1=loop all, 2=loop one)
    current_song_title : str
        Title of currently playing song
    current_song_artist : str
        Artist of currently playing song
    current_song_length : str
        Total duration of current song (formatted as M:SS)
    current_song_position : str
        Current playback position (formatted as M:SS)
    song_length : int
        Total duration of current song in seconds
    seek_offset : float
        Position in seconds where seeking/playback started
    last_update_time : int
        Pygame ticks timestamp of last position update
    AUDIO_OK : bool
        True if pygame.mixer initialized successfully
    
    Examples
    --------
    >>> player_window = Player_Window()
    >>> audio = AudioPlayer(player_window)
    >>> audio.add_songs()  # Opens file dialog
    >>> audio.toggle_play_pause()  # Starts playback
    """

    def __init__(self, player_window):
        """
        Initialize the audio player with pygame mixer and default values.
        
        Parameters
        ----------
        player_window : Player_Window
            The main player window instance that contains UI elements
            
        Notes
        -----
        Automatically initializes pygame.mixer and sets up the music end event.
        If mixer initialization fails, AUDIO_OK is set to False and audio
        operations will be disabled.
        """
        try:
            pygame.mixer.init()
            self.AUDIO_OK = True
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1) 
        except Exception as e:
            self.AUDIO_OK = False
            print(f"Error initializing mixer: {e}")

        self.player_window = player_window 
        self.root = player_window.root
        self.pause_bnt = player_window.pause_bnt
        self.play_bnt = player_window.play_bnt
        self.current_icon = player_window.current_icon

        self.playlist = []
        self.index = 0
        self.is_playing = False
        self.paused = False

        # Loop modes: 0 = no loop, 1 = loop all, 2 = loop one
        self.loop_mode = 0

        # Metadata placeholders
        self.current_song_title = ""
        self.current_song_artist = ""
        self.current_song_length = "0:00"
        self.current_song_position = "0:00"
        self.song_length = 0


        self.seek_offset = 0
        self.last_update_time = 0

          
    def _play_music(self, song):
        """
        Load and play a song file.
        
        This is an internal method that loads an MP3 file into pygame.mixer,
        starts playback, resets seek position, and loads metadata.
        
        Parameters
        ----------
        song : str
            Full file path to the MP3 file to play
            
        Notes
        -----
        - Resets seek_offset and last_update_time for accurate position tracking
        - Automatically calls _song_meta_data() to extract song information
        - Only executes if AUDIO_OK is True
        """
        if self.AUDIO_OK:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.is_playing = True
            self.paused = False
            self.seek_offset = 0
            self.last_update_time = pygame.time.get_ticks()
            self._song_meta_data()

    def _pause_music(self):
        """
        Pause the currently playing music.
        
        Sets the paused flag and updates is_playing state.
        Does not reset playback position - use toggle_play_pause() 
        to resume from the same position.
        
        Notes
        -----
        Only executes if AUDIO_OK is True
        """
        if self.AUDIO_OK:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.paused = True

    def toggle_play_pause(self):
        """
        Toggle between play and pause states.
        
        If currently playing, pauses the music. If paused or stopped,
        resumes or starts playback. Automatically updates the play/pause
        button icon in the UI.
        
        Returns
        -------
        None
        
        Notes
        -----
        - Does nothing if playlist is empty
        - If paused, resumes from current position
        - If stopped, starts playing current track from beginning
        - Updates both self.current_icon and player_window.current_icon
        """
        # If playlist is empty, nothing to play — return early
        if not self.playlist:
            return

        if self.is_playing:
            # Pause
            try:
                self._pause_music()
            except Exception:
                pass
            self.is_playing = False
            self.current_icon = self.play_bnt
        else:
            # If music was never started, start it; otherwise unpause
            try:
                if not self.paused:
                    self._play_music(self.playlist[self.index])
                else:
                    pygame.mixer.music.unpause()
                    self.paused = False
            except Exception:
                self._play_music(self.playlist[self.index])

            self.is_playing = True
            self.current_icon = self.pause_bnt

    def add_songs(self):
        """
        Open file dialog to select MP3 files and add them to playlist.
        
        Opens a native file dialog allowing the user to select one or more
        MP3 files. Selected files replace the current playlist and playback
        starts immediately with the first selected track.
        
        Notes
        -----
        - Replaces entire playlist (does not append)
        - Automatically starts playing first track
        - Updates UI to show pause button
        - Prints loaded playlist to console
        """
        files = filedialog.askopenfilenames(
            parent=self.root,
            filetypes=[("MP3 Files", "*.mp3")],
            title="Select Songs"
        )

        if files:
            self.playlist = list(files)
            self._play_music(self.playlist[self.index])
            self.is_playing = True
            self.current_icon = self.pause_bnt

    def next_song(self):
        """
        Skip to the next track in the playlist.
        
        Advances to the next song in the playlist and starts playing it.
        Wraps around to the first track if currently on the last track.
        
        Returns
        -------
        None
        
        Notes
        -----
        - Does nothing if playlist is empty
        - Automatically wraps to beginning of playlist
        - Always starts playing (even if previously paused)
        """
        if not self.playlist:
            return
        self.index = (self.index + 1) % len(self.playlist)
        self._play_music(self.playlist[self.index])
        self.is_playing = True
        self.current_icon = self.pause_bnt

    def previous_song(self):
        """
        Go back to the previous track in the playlist.
        
        Moves to the previous song in the playlist and starts playing it.
        Wraps around to the last track if currently on the first track.
        
        Returns
        -------
        None
        
        Notes
        -----
        - Does nothing if playlist is empty
        - Automatically wraps to end of playlist
        - Always starts playing (even if previously paused)
        """
        if not self.playlist:
            return
        self.index = (self.index - 1) % len(self.playlist)
        self._play_music(self.playlist[self.index])
        self.is_playing = True
        self.current_icon = self.pause_bnt

    def change_volume(self, value: float):
        """
        Set the audio output volume.
        
        Parameters
        ----------
        value : float
            Volume level between 0.0 (silent) and 1.0 (maximum volume)
            
        Notes
        -----
        Called by the volume slider's callback function.
        Prints volume value to console for debugging.
        """
        pygame.mixer.music.set_volume(value)
        

    def _song_meta_data(self):
        """
        Extract and store metadata from the current song.
        
        Reads ID3 tags from the current MP3 file using mutagen library
        to extract title, artist, and duration. Updates all relevant
        instance variables with the extracted information.
        
        Notes
        -----
        - Safely handles missing metadata by using empty strings
        - Calculates and formats song duration as M:SS
        - Silently fails on any exception (corrupted files, missing tags)
        - Updates: current_song_title, current_song_artist, 
          current_song_length, song_length
        """

        try:
            audio_file = MP3(self.playlist[self.index], ID3=EasyID3)

            title_list = audio_file.get("title")
            artist_list = audio_file.get("artist")
            title = title_list[0] if title_list else ""
            artist = artist_list[0] if artist_list else ""

            seconds = int(audio_file.info.length)
            self.song_length = seconds
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            duration = f"{minutes}:{remaining_seconds:02}"

            self.current_song_title = title
            self.current_song_artist = artist
            self.current_song_length = duration

        except Exception:
            pass

    def adjust_song(self, value):
        """
        Seek to a specific position in the current song.
        
        Called by the progress slider to jump to a different position
        in the currently playing song. Handles both playing and paused states.
        
        Parameters
        ----------
        value : float
            Normalized position between 0.0 (start) and 1.0 (end)
            
        Notes
        -----
        - Does nothing if playlist is empty or song_length is 0
        - Converts normalized value to seconds based on song length
        - Updates seek_offset and last_update_time for position tracking
        - If not playing, starts playback from the seek position
        - If paused, resumes playback from the seek position
        - Prints debug information about seek position
        """
        # Don't do anything if no song is loaded
        if not self.playlist or self.song_length == 0:
            return
        
        # Convert slider value (0-1) to song position in seconds
        position_seconds = value * self.song_length
        
        
        try:
            # Store the seek position
            self.seek_offset = position_seconds
            self.last_update_time = pygame.time.get_ticks()
            
            # Set the position in the song
            pygame.mixer.music.set_pos(position_seconds)
            
            # Resume playback if paused
            if not self.is_playing:
                pygame.mixer.music.play(start=position_seconds)
                self.is_playing = True
                self.paused = False
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
        except pygame.error as e:
            print(f"Error adjusting song position: {e}")
    
    def get_current_position(self):
        """
        Get the current playback position in seconds.
        
        Calculates the current position by adding the elapsed time since
        the last seek to the seek offset position. Returns the paused
        position if playback is paused.
        
        Returns
        -------
        float
            Current position in seconds, capped at song_length
            
        Notes
        -----
        - Returns 0 if no song is loaded
        - Returns seek_offset if paused
        - Calculates real-time position during playback
        - Never exceeds total song length
        """
        if not self.is_playing or self.paused:
            return self.seek_offset
        
        # Calculate position: seek_offset + time elapsed since seek
        elapsed = (pygame.time.get_ticks() - self.last_update_time) / 1000.0
        current_pos = self.seek_offset + elapsed
        
        return min(current_pos, self.song_length)

    def update_current_position(self):
        """
        Update the formatted current position string.
        
        Called every frame to update the displayed current position.
        Converts the numeric position from get_current_position() into
        a formatted string (M:SS) for display in the UI.
        
        Notes
        -----
        - Updates current_song_position attribute
        - Shows "0:00" if no playlist or song_length is 0
        - Should be called in the main game loop
        """
        if self.playlist and self.song_length > 0:
            current_seconds = self.get_current_position()
            self.current_song_position = self.convert_sec_min(current_seconds)
        else:
            self.current_song_position = "0:00"

    def convert_sec_min(self, seconds):
        """
        Convert seconds to minutes:seconds format.
        
        Parameters
        ----------
        seconds : float or int
            Time duration in seconds
            
        Returns
        -------
        str
            Formatted time string as "M:SS" (e.g., "3:45", "0:08", "12:30")
            
        Examples
        --------
        >>> audio.convert_sec_min(0)
        '0:00'
        >>> audio.convert_sec_min(65)
        '1:05'
        >>> audio.convert_sec_min(3661)
        '61:01'
        """
        minutes = int(seconds) // 60
        remaining_seconds = int(seconds) % 60
        return f"{minutes}:{remaining_seconds:02}"

    def toggle_loop_mode(self):
        """
        Cycle through loop modes: off → loop all → loop one → off.
        
        Changes the loop behavior and returns the new mode for UI updates.
        
        Returns
        -------
        int
            The new loop mode (0=off, 1=loop all, 2=loop one)
            
        Notes
        -----
        Loop modes:
        - 0 (Loop Off): Song stops at end, playback stops
        - 1 (Loop All): Automatically plays next song, wraps to beginning
        - 2 (Loop One): Repeats the current song indefinitely
        
        Prints the current mode name to console for debugging.
        """
        self.loop_mode = (self.loop_mode + 1) % 3
        
        mode_names = ["Loop Off", "Loop All", "Loop One"]
        
        return self.loop_mode

    def on_song_end(self):
        """
        Handle the end of song event based on loop mode.
        
        Called automatically when pygame.USEREVENT + 1 is triggered
        (when a song finishes playing). Behavior depends on current loop_mode:
        
        - Loop One (2): Replays the current song
        - Loop All (1): Advances to next song in playlist
        - Loop Off (0): Stops playback and shows play button
        
        Notes
        -----
        - Updates UI icons appropriately for each mode
        - Resets playback state when stopping (loop off)
        - Should be called from the event loop when music ends
        """
        if self.loop_mode == 2:
            # Loop one - replay current song
            self._play_music(self.playlist[self.index])
            self.player_window.current_icon = self.pause_bnt
            self.current_icon = self.pause_bnt
        elif self.loop_mode == 1:
            # Loop all - play next song
            self.next_song()
        else:
            # No loop - stop playback
            self.is_playing = False
            self.paused = False
            self.seek_offset = 0
            self.last_update_time = 0
            
            # Change icon to play button
            self.player_window.current_icon = self.play_bnt
            self.current_icon = self.play_bnt







