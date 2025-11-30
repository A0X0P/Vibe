import pygame



class Buttons:
    """
    Interactive UI button with image, click detection, and press overlay.
    
    Provides visual feedback with a dark overlay when pressed and reliable
    click detection that only triggers on release inside the button area.
    
    Attributes
    ----------
    img : pygame.Surface
        The button's image
    rect : pygame.Rect
        Button's position and collision rectangle
    is_down : bool
        True when mouse button is pressed down on this button
    was_released_inside : bool
        UNUSED - can be removed
    dark_overlay : pygame.Surface
        Semi-transparent dark overlay shown when button is pressed
        
    Examples
    --------
    >>> play_btn = Buttons(100, 200, "images/play.png")
    >>> play_btn.draw(screen)
    >>> if play_btn.was_clicked(event):
    ...     start_music()
    """

    def __init__(self, x_pos, y_pos, img_path):
        """
        Create a button at specified position with an image.
        
        Parameters
        ----------
        x_pos : int
            X coordinate of button center
        y_pos : int
            Y coordinate of button center
        img_path : str
            Path to button image file
            
        Notes
        -----
        - Button rect is centered at (x_pos, y_pos)
        - Dark overlay is created with 120 alpha (semi-transparent)
        - Overlay has 5-pixel border radius for rounded corners
        """
        # Load image
        self.img = pygame.image.load(img_path).convert_alpha()
        self.rect = self.img.get_rect(center=(x_pos, y_pos))

        # Press state
        self.is_down = False
    
        # Dark overlay surface
        self.dark_overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.dark_overlay,
            (0, 0, 0, 120),
            self.dark_overlay.get_rect(),
            border_radius=5
        )

    def draw(self, screen):
        """
        Render the button to the screen, with overlay if pressed.
        
        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the button on
            
        Notes
        -----
        - Always draws the base button image
        - Draws dark overlay on top if is_down is True
        - Should be called every frame in the main loop
        """
        screen.blit(self.img, self.rect)

        if self.is_down:
            screen.blit(self.dark_overlay, self.rect.topleft)

    def handle_overlay(self, event):
        """
        Update button press state for visual feedback.
        
        Parameters
        ----------
        event : pygame.event.Event
            The event to process
            
        Notes
        -----
        - Sets is_down to True on MOUSEBUTTONDOWN inside button
        - Clears is_down on any MOUSEBUTTONUP (regardless of position)
        - This method only handles visual state, not click logic
        - Should be called for every event in the event loop
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_down = False

    def was_clicked(self, event) -> bool:
        """
        Check if button was clicked (pressed and released inside).
        
        Parameters
        ----------
        event : pygame.event.Event
            The event to check
            
        Returns
        -------
        bool
            True if this is a MOUSEBUTTONUP event inside the button,
            False otherwise
            
        Notes
        -----
        - Only returns True on mouse button RELEASE (not press)
        - Mouse must be released inside the button area
        - This is the definitive click detection method
        - Should be checked in event loop after handle_overlay()
        
        Examples
        --------
        >>> for event in pygame.event.get():
        ...     button.handle_overlay(event)
        ...     if button.was_clicked(event):
        ...         print("Button clicked!")
        """
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        return False






