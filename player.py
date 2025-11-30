"""Module providing a Music Player class with Pygame UI and Tkinter dialogs."""
import os
import sys
import math

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import ctypes
import tkinter as tk

from settings import Settings
from buttons import Buttons
from slider import Slider_UI
from audio import AudioPlayer


class Player_Window:
    """
    Main music player window with Pygame UI and Tkinter file dialogs.
    
    This class manages the entire player interface including the animated
    vinyl platter, tone arm needle, playback controls, volume/progress sliders,
    scrolling text display, and options menu.
    
    Attributes
    ----------
    screen : pygame.Surface
        Main display surface for rendering
    root : tk.Tk
        Hidden Tkinter root for file dialogs
    audio : AudioPlayer
        Audio playback controller
    volume_slider : Slider_UI
        Volume control slider (0.0 to 1.0)
    music_slider : Slider_UI
        Song progress/seek slider (0.0 to 1.0)
    angle : float
        Current rotation angle of vinyl platter (0-360)
    needle_angle : float
        Current angle of tone arm needle
    flip_state : bool
        True when options menu is open
    
    Notes
    -----
    The player uses a 60 FPS game loop for smooth animations and updates.
    All UI elements are positioned using absolute pixel coordinates.
    """
    
    def __init__(self):
        """
        Initialize the music player window and all UI components.
        
        Sets up:
        - Pygame display window
        - Tkinter root for file dialogs (hidden)
        - Background images
        - All buttons (play, pause, next, previous, loop, menu)
        - Volume and progress sliders
        - Audio player instance
        - Animation variables for platter and needle
        
        Notes
        -----
        - Attempts to set DPI awareness on Windows
        - Loads all images from Images/ directory
        - Creates rounded corners for options menu
        """
        pygame.init()
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

        player_settings = Settings()

        # Tkinter root for file dialogs (hidden)
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.iconphoto(False, tk.PhotoImage(file="Images/set_icon.png"))
        self.root.attributes("-topmost", True)

        # Main Pygame Window
        self.screen = pygame.display.set_mode(
            (player_settings.screen_width, player_settings.screen_height),
           pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.screen = pygame.display.get_surface()
        pygame.display.set_caption("Vibe")
        pygame.display.set_icon(pygame.image.load("Images/set_icon.png"))

        # Background image / color
        self.background_img = pygame.image.load("Images/Frame_1.png").convert()
        self.background_img = pygame.transform.scale(
            self.background_img,
            (player_settings.screen_width, player_settings.screen_height)
        )
        self.background_color = player_settings.screen_colour

        options_menu_img = pygame.image.load("Images/Frame_2.png")
        self.rounded_img = self.make_rounded_image(options_menu_img, 20)
        self.flip_state = False

        # Buttons
        self._buttons_init()

        # Playlist and audio
        self.audio = AudioPlayer(self)

        # Sliders
        self.volume_slider = Slider_UI(
            rect=pygame.Rect(785, 539, 255, 10),
            on_click=self.audio.change_volume,
            value=0.5
        )
        self.music_slider = Slider_UI(
            rect=pygame.Rect(745.6, 366, 330, 7),
            on_click=self.audio.adjust_song,
            value=0
        )

        # Platter rotation
        self.angle = 0
        
        # Needle rotation
        self.needle_angle = 90
        self.target_needle_angle_playing = 129
        self.target_needle_angle_paused = 90

        # Scrolling text
        self.scroll_area_x = 882
        self.scroll_area_width = pygame.image.load("Images/song_name_Rectangle.png").get_width() - 39
        self.scroll_text_x = self.scroll_area_x
        self.scroll_speed = 0.25

    def _buttons_init(self):
        """
        Initialize all button objects with their positions and images.
        
        Creates instances of:
        - Play/pause toggle buttons
        - Next/previous track buttons
        - Options menu (ellipse) button
        - Add songs and cancel buttons
        - Loop mode buttons (off, all, one) with background
        
        Notes
        -----
        All button positions are hardcoded pixel coordinates.
        current_icon starts as play_bnt (play button).
        current_loop_icon starts as loop_off_bnt (loop off).
        """
        self.play_bnt = Buttons(910, 450, "Images/play.png")
        self.pause_bnt = Buttons(910, 450, "Images/pause.png")
        self.current_icon = self.play_bnt

        self.next_bnt = Buttons(1050, 452, "Images/next.png")
        self.previous_bnt = Buttons(772, 452, "Images/previous.png")
        self.ellipse_bnt = Buttons(45, 35, "Images/ellipse.png")
        self.cancel_bnt = Buttons(258, 120, "Images/cancel.png")
        self.add_button = Buttons(258, 52, "Images/add.png")

        # Loop buttons
        self.loop_off_bnt = Buttons(1100, 50, "Images/loop_off.png")
        self.loop_all_bnt = Buttons(1100, 50, "Images/loop_all.png")
        self.loop_one_bnt = Buttons(1100, 50, "Images/loop_one.png")
        self.loop_background = Buttons(1100, 50, "Images/loop_bg.png")

        self.current_loop_icon = self.loop_off_bnt

    def start_player(self):
        """
        Start the main game loop at 60 FPS.
        
        This method runs indefinitely until the user closes the window.
        Each frame:
        1. Draws background and UI elements
        2. Updates song position display
        3. Rotates platter if playing
        4. Animates needle position
        5. Updates progress slider
        6. Processes all user input events
        
        Notes
        -----
        - Runs at 60 FPS using pygame.time.Clock
        - Handles all mouse/keyboard events
        - Exits cleanly with pygame.quit() and sys.exit()
        """
        clock = pygame.time.Clock()
        
        while True:
            # Draw background and UI
            self.screen.fill(self.background_color)
            self.screen.blit(self.background_img, (0, 0))

            self.audio.update_current_position() 
            
            self._rotate_platter()
            self._display_music_meta_data()
            self._move_needle()

            # Draw UI elements
            self._draw_buttons()

            # Update progress slider during playback
            if self.audio.is_playing and not self.music_slider.dragging:
                if self.audio.song_length > 0:
                    current_pos = self.audio.get_current_position()
                    slider_value = min(1.0, current_pos / self.audio.song_length)
                    self.music_slider.value = slider_value
            
            pygame.display.flip()
            clock.tick(60)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Detect when music ends
                if event.type == pygame.USEREVENT + 1:
                    self.audio.on_song_end()

                # Update overlay/press state
                self.current_icon.handle_overlay(event)
                self.next_bnt.handle_overlay(event)
                self.previous_bnt.handle_overlay(event)
                self.ellipse_bnt.handle_overlay(event)
                self.add_button.handle_overlay(event)
                self.cancel_bnt.handle_overlay(event)
                self.loop_background.handle_overlay(event)
                self.current_loop_icon.handle_overlay(event)

                # Sliders
                self.volume_slider.handle_event(event)
                self.music_slider.handle_event(event)

                # Button clicks
                try:
                    if self.current_icon.was_clicked(event):
                        self.audio.toggle_play_pause()
                except AttributeError:
                    pass

                if self.next_bnt.was_clicked(event):
                    self.audio.next_song()
                if self.previous_bnt.was_clicked(event):
                    self.audio.previous_song()

                # Loop button click handler
                if self.current_loop_icon.was_clicked(event):
                    loop_mode = self.audio.toggle_loop_mode()
                    if loop_mode == 0:
                        self.current_loop_icon = self.loop_off_bnt
                    elif loop_mode == 1:
                        self.current_loop_icon = self.loop_all_bnt
                    else:
                        self.current_loop_icon = self.loop_one_bnt

                if self.add_button.was_clicked(event):
                    if self.flip_state:
                        self.audio.add_songs()

                if self.cancel_bnt.was_clicked(event):
                    self.close_options_menu()

                if self.ellipse_bnt.was_clicked(event):
                    self.open_options_menu()

    def _draw_buttons(self):
        """
        Render all visible buttons and sliders to the screen.
        
        Draws:
        - Current play/pause icon
        - Next/previous buttons
        - Loop button background and current loop icon
        - Options menu overlay (if open)
        - Add songs and cancel buttons (if menu open)
        - Ellipse menu button (if menu closed)
        - Volume and progress sliders
        
        Notes
        -----
        Drawing order matters - items drawn last appear on top.
        Options menu overlay is only drawn when flip_state is True.
        """
        self.audio.current_icon.draw(self.screen)
        self.next_bnt.draw(self.screen)
        self.previous_bnt.draw(self.screen)
        self.loop_background.draw(self.screen)
        self.current_loop_icon.draw(self.screen)

        if self.flip_state:
            self.screen.blit(self.rounded_img, (11, 0))
            self.add_button.draw(self.screen)
            self.cancel_bnt.draw(self.screen)
        else:
            self.ellipse_bnt.draw(self.screen)

        self.volume_slider.draw(self.screen)
        self.music_slider.draw(self.screen)

    def _rotate_platter(self):
        """
        Rotate and render the vinyl platter graphic.
        
        Loads the disk image, rotates it by the current angle if music
        is playing, and blits it to the screen at the platter position.
        
        Notes
        -----
        - Platter only rotates when audio.is_playing is True
        - Rotation angle increments by 1 degree per frame (60°/second)
        - Angle wraps around at 360 degrees
        - Image is loaded fresh each frame (could be optimized by caching)
        """
        platter = pygame.image.load(r"Images/disk.png").convert_alpha()
        
        if self.audio.is_playing:
            self.angle = (self.angle + 1) % 360
            
        rotated_platter = pygame.transform.rotate(platter, self.angle)
        platter_rect = platter.get_rect(center=(328, 367))
        r_rect = rotated_platter.get_rect(center=platter_rect.center)
        self.screen.blit(rotated_platter, r_rect)

    def _move_needle(self):
        """
        Animate and render the tonearm needle.
        
        Smoothly interpolates the needle between two positions:
        - Playing: angled down onto the platter (129°)
        - Paused/Stopped: lifted away from platter (90°)
        
        Uses easing for smooth animation and rotates around a fixed
        pivot point to simulate realistic tonearm movement.
        
        Notes
        -----
        - Needle angle smoothly transitions with 15% easing per frame
        - Pivot point is offset from platter center
        - Image is loaded fresh each frame (could be optimized)
        - Rotation and positioning use trigonometry for realistic movement
        """
        needle_img = pygame.image.load(r"Images/needle.png").convert_alpha()
       
        platter_center = (328, 367)
        
        # Determine target angle based on playback state
        target_angle = self.target_needle_angle_playing if self.audio.is_playing else self.target_needle_angle_paused
        
        # Smoothly interpolate to target angle
        angle_diff = target_angle - self.needle_angle
        if abs(angle_diff) > 0.1:
            self.needle_angle += angle_diff * 0.15
        else:
            self.needle_angle = target_angle
        
        # Fixed pivot point
        pivot_x = platter_center[0] + 212
        pivot_y = platter_center[1] - 32
        
        rad_angle = math.radians(self.needle_angle)
        needle_length = needle_img.get_height()
        
        # Rotate the needle image
        rotated_needle = pygame.transform.rotate(needle_img, -self.needle_angle + 90)

        # Position with pivot offset
        needle_rect = rotated_needle.get_rect()
        needle_rect.center = (pivot_x, pivot_y)
        
        offset_x = math.cos(rad_angle) * (needle_length/4)
        offset_y = math.sin(rad_angle) * (needle_length/4)
        
        needle_rect.centerx = int(pivot_x + offset_x)
        needle_rect.centery = int(pivot_y + offset_y)
        
        self.screen.blit(rotated_needle, needle_rect)


    def render_music_duration(self, text: str, font_size: int, x: int, y: int):
        """
        Render time duration text at specified screen coordinates.
        
        Parameters
        ----------
        text : str
            The time string to display (e.g., "3:45")
        font_size : int
            Font size in pixels
        x : int
            X coordinate for text position
        y : int
            Y coordinate for text position
            
        Notes
        -----
        - Uses system default font (None)
        - Text is rendered in black (0, 0, 0)
        - Called to display both current position and total duration
        """
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))


    def _render_text(self, text: str, font_size: int, y: int):
        """
        Render horizontally scrolling text in a fixed-width area.
        
        Creates a clipped surface for text scrolling, used for song titles
        and artist names that may be too long to fit on screen.
        
        Parameters
        ----------
        text : str
            The text to display and scroll
        font_size : int
            Font size in pixels
        y : int
            Y coordinate for the text area
            
        Notes
        -----
        - Text scrolls continuously from right to left
        - Wraps around when fully scrolled off screen
        - Scroll speed controlled by self.scroll_speed (0.25 px/frame)
        - Uses white background for clipped area
        - Text position resets when it scrolls completely off left side
        """
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_width = text_surface.get_width()

        scroll_surface = pygame.Surface((self.scroll_area_width, font_size))
        scroll_surface.fill((255, 255, 255))
        scroll_surface.blit(text_surface, (self.scroll_text_x - self.scroll_area_x, 8))
        self.screen.blit(scroll_surface, (self.scroll_area_x, y))

        # Update scroll position
        self.scroll_text_x -= self.scroll_speed
        if self.scroll_text_x < self.scroll_area_x - text_width:
            self.scroll_text_x = self.scroll_area_x + self.scroll_area_width

    def _display_music_meta_data(self):
        """
        Display song metadata and playback time information.
        
        Renders: 
        - Song title (scrolling if too long)
        - Artist name (scrolling if too long)
        - Current playback position (left side)
        - Total song duration (right side)
        
        Shows "Nothing Playing" and "Unknown Artist" when no song is loaded
        or metadata is unavailable.
        
        Notes
        -----
        - Title and artist use scrolling text for long names
        - Times are displayed at fixed positions below progress bar
        - All text pulled from AudioPlayer instance variables
        """
        if not self.audio.current_song_title and not self.audio.current_song_artist:
            self._render_text("Nothing Playing.", font_size=30, y=95)
            self._render_text("Unknown Artist.", font_size=25, y=147)
        else:
            self._render_text(str(self.audio.current_song_title), font_size=30, y=95)
            self._render_text(str(self.audio.current_song_artist), font_size=25, y=147)

        # LEFT side - current position (updates in real-time)
        self.render_music_duration(str(self.audio.current_song_position), 20, 743, 385)
        
        # RIGHT side - total length (stays constant)
        self.render_music_duration(str(self.audio.current_song_length), 20, 1055, 385)

    def open_options_menu(self):
        """
        Show the options menu overlay.
        
        Sets flip_state to True, which causes _draw_buttons() to render
        the rounded menu overlay with add songs and cancel buttons instead
        of the normal ellipse menu button.
        """
        self.flip_state = True

    def close_options_menu(self):
        """
        Hide the options menu overlay.
        
        Sets flip_state to False, which causes _draw_buttons() to render
        the normal ellipse menu button instead of the options overlay.
        """
        self.flip_state = False

    def make_rounded_image(self, img: pygame.Surface, radius: int):
        """
        Create a version of an image with rounded corners.
        
        Parameters
        ----------
        img : pygame.Surface
            The original image to add rounded corners to
        radius : int
            Corner radius in pixels
            
        Returns
        -------
        pygame.Surface
            New surface with rounded corners and transparency
            
        Notes
        -----
        - Uses alpha blending to create smooth rounded corners
        - Original image is not modified
        - Returned surface has SRCALPHA flag for transparency
        - Used for the options menu overlay
        """
        width, height = img.get_width(), img.get_height()
        
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            (0, 0, width, height),
            border_radius=radius
        )
        
        rounded = pygame.Surface((width, height), pygame.SRCALPHA)
        rounded.blit(img, (0, 0))
        rounded.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        return rounded
    





