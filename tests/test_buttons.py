"""Unit tests for Buttons component."""
import os
import pytest
import pygame


from buttons import Buttons


@pytest.fixture(scope="module", autouse=True)
def setup_pygame():
    """Initialize pygame once for all button tests."""
    pygame.init()

    # Create a display and # Create a dummy image for testing
    pygame.display.set_mode((1, 1))  
    
    test_surface = pygame.Surface((50, 50))
    pygame.image.save(test_surface, "test_button.png")
    yield
    pygame.quit()
    if os.path.exists("test_button.png"):
        os.remove("test_button.png")


@pytest.fixture
def button():
    """Create a button instance for testing."""
    return Buttons(100, 100, "test_button.png")


class TestButtonInitialization:
    """Test button initialization."""
    
    def test_initialization(self, button):
        """Test button initializes correctly."""
        assert button.rect.center == (100, 100)
        assert button.is_down is False
    
    def test_button_has_image(self, button):
        """Test button loads image correctly."""
        assert button.img is not None
        assert button.img.get_width() > 0
        assert button.img.get_height() > 0
    
    def test_button_has_dark_overlay(self, button):
        """Test button creates dark overlay."""
        assert button.dark_overlay is not None
        assert button.dark_overlay.get_size() == button.rect.size


class TestButtonPressState:
    """Test button press state management."""
    
    def test_mouse_down_sets_is_down(self, button):
        """Test mouse down on button sets is_down to True."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'pos': (100, 100)}
        )
        
        button.handle_overlay(event)
        assert button.is_down is True
    
    def test_mouse_up_clears_is_down(self, button):
        """Test mouse up clears is_down state."""
        button.is_down = True
        
        event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {'pos': (100, 100)}
        )
        
        button.handle_overlay(event)
        assert button.is_down is False
    
    def test_mouse_down_outside_does_not_set_is_down(self, button):
        """Test mouse down outside button doesn't set is_down."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'pos': (500, 500)}
        )
        
        button.handle_overlay(event)
        assert button.is_down is False
    
    def test_mouse_up_clears_is_down_even_if_outside(self, button):
        """Test mouse up clears is_down regardless of position."""
        button.is_down = True
        
        event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {'pos': (500, 500)}
        )
        
        button.handle_overlay(event)
        assert button.is_down is False


class TestButtonClickDetection:
    """Test button click detection."""
    
    def test_was_clicked_returns_true_on_release_inside(self, button):
        """Test was_clicked returns True when released inside."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {'pos': (100, 100)}
        )
        
        result = button.was_clicked(event)
        assert result is True
    
    def test_was_clicked_returns_false_on_release_outside(self, button):
        """Test was_clicked returns False when released outside."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {'pos': (500, 500)}
        )
        
        result = button.was_clicked(event)
        assert result is False
    
    def test_was_clicked_returns_false_on_other_events(self, button):
        """Test was_clicked returns False for non-MOUSEBUTTONUP events."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'pos': (100, 100)}
        )
        
        result = button.was_clicked(event)
        assert result is False
    
    def test_was_clicked_on_button_edge(self, button):
        """Test click detection at button edges."""
        # Get button boundaries
        left = button.rect.left
        right = button.rect.right
        top = button.rect.top
        bottom = button.rect.bottom
        
        # Test corners
        for pos in [(left, top), (right-1, top), (left, bottom-1), (right-1, bottom-1)]:
            event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': pos})
            assert button.was_clicked(event) is True