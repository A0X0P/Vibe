import pygame
from typing import Callable

from settings import Settings



class Slider_UI:
    """
    A horizontal slider widget for Pygame UI.

    The slider supports:
    - Click & drag interaction
    - Value output between 0.0 and 1.0
    - A callback function triggered on value change
    - Customizable colors via Settings
    """

    def __init__(self, rect: pygame.Rect,  on_click: Callable[[float], None], value: float = 0.0):
        """
        Create a slider control.

        Parameters
        ----------
        rect : pygame.Rect
            The rectangular area where the slider is drawn.
        on_click : Callable[[float], None]
            A callback triggered whenever the slider's value changes.
        value : float, optional
            Initial slider value in [0.0, 1.0], by default 0.0.
        """
        self.rect = rect
        self.value = value
        self.on_click = on_click
        self.dragging = False

        # Load shared UI settings
        self.slider_settings = Settings()

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse interactions with the slider.

        Parameters
        ----------
        event : pygame.event.Event
            The current event received from Pygame.
        """

        # Start dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.dragging = True
            self._update_slider_position(event.pos)

        # Continue dragging
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_slider_position(event.pos)

        # Stop dragging 
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False


    def _update_slider_position(self, pos: tuple[int, int]) -> None:
        """
        Update the slider's internal value based on mouse movement.

        Parameters
        ----------
        pos : tuple[int, int]
            The (x, y) mouse position.
        """

        # Prevent division by zero or invalid space
        if self.rect.width <= 0:
            return
    
        # Convert absolute mouse X into a normalized slider value
        relative_x = pos[0] - self.rect.x
        new_value = max(0.0, min(1.0, relative_x / self.rect.width))

        # Only trigger callback if value truly changed
        if abs(new_value - self.value) > 1e-6:
            self.value = new_value
            self.on_click(self.value)


    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the slider background, filled portion, and knob.

        Parameters
        ----------
        surface : pygame.Surface
            The Pygame surface on which to render the slider.
        """

        # knob size (square)
        size = max(6, self.rect.height // 2) * 2
        radius = size // 4

        # Background bar
        pygame.draw.rect(surface, self.slider_settings.slider_bg_color , self.rect, border_radius=radius)

        # Filled section
        fill_width = int(self.rect.width * self.value)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.slider_settings.slider_filled_color, fill_rect, border_radius=radius)
        
        # Knob placement
        knob_x = self.rect.x + fill_width
        knob_x = max(self.rect.x, min(knob_x, self.rect.right))
        knob_rect = pygame.Rect( knob_x - size // 2,self.rect.centery - size // 2, size, size)
        pygame.draw.rect(surface, self.slider_settings.slider_knob_color, knob_rect, border_radius=radius)
        









        
