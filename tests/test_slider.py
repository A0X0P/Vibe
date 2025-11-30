"""Unit tests for Slider_UI component."""
from unittest.mock import Mock
import pytest
import pygame

from slider import Slider_UI


@pytest.fixture(autouse=True)
def setup_pygame():
    """Initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_callback():
    """Create a mock callback function."""
    return Mock()


@pytest.fixture
def slider(mock_callback):
    """Create a slider instance for testing."""
    return Slider_UI(
        rect=pygame.Rect(0, 0, 100, 10),
        on_click=mock_callback,
        value=0.5
    )


class TestSliderInitialization:
    """Test slider initialization."""
    
    def test_initialization(self, slider, mock_callback):
        """Test slider initializes with correct values."""
        assert slider.rect == pygame.Rect(0, 0, 100, 10)
        assert slider.value == 0.5
        assert slider.on_click == mock_callback
        assert slider.dragging is False


class TestSliderValueCalculation:
    """Test slider value calculations."""
    
    def test_update_slider_position_calculates_correctly(self, slider, mock_callback):
        """Test slider value calculation from mouse position."""
        # Click at 75% position (x=75 in a 100-width slider)
        slider._update_slider_position((75, 5))
        
        # Should be called with 0.75
        mock_callback.assert_called_once()
        assert 0.74 < slider.value < 0.76
    
    def test_update_slider_position_clamps_to_zero(self, slider, mock_callback):
        """Test slider clamps negative positions to 0."""
        slider._update_slider_position((-10, 5))
        assert slider.value == 0.0
    
    def test_update_slider_position_clamps_to_one(self, slider, mock_callback):
        """Test slider clamps positions beyond width to 1."""
        slider._update_slider_position((150, 5))
        assert slider.value == 1.0
    
    def test_update_slider_position_at_exact_positions(self, slider, mock_callback):
        """Test slider at exact 0%, 50%, 100%."""
        slider._update_slider_position((0, 5))
        assert slider.value == 0.0
        
        slider._update_slider_position((50, 5))
        assert abs(slider.value - 0.5) < 0.01
        
        slider._update_slider_position((100, 5))
        assert slider.value == 1.0


class TestSliderEventHandling:
    """Test slider event handling."""
    
    def test_handle_event_mouse_down_starts_dragging(self, slider):
        """Test mouse down on slider starts dragging."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': (50, 5)}
        )
        
        slider.handle_event(event)
        assert slider.dragging is True
    
    def test_handle_event_mouse_up_stops_dragging(self, slider):
        """Test mouse up stops dragging."""
        slider.dragging = True
        
        event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {'button': 1, 'pos': (50, 5)}
        )
        
        slider.handle_event(event)
        assert slider.dragging is False
    
    def test_handle_event_mouse_down_outside_does_nothing(self, slider):
        """Test mouse down outside slider doesn't start dragging."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 1, 'pos': (200, 200)}
        )
        
        slider.handle_event(event)
        assert slider.dragging is False
    
    def test_handle_event_right_click_ignored(self, slider):
        """Test right mouse button is ignored."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {'button': 3, 'pos': (50, 5)}
        )
        
        slider.handle_event(event)
        assert slider.dragging is False
    
    def test_handle_event_motion_while_dragging(self, slider, mock_callback):
        """Test mouse motion updates value while dragging."""
        slider.dragging = True
        
        event = pygame.event.Event(
            pygame.MOUSEMOTION,
            {'pos': (80, 5)}
        )
        
        slider.handle_event(event)
        assert 0.79 < slider.value < 0.81


class TestSliderCallback:
    """Test slider callback behavior."""
    
    def test_callback_not_called_if_value_unchanged(self, slider, mock_callback):
        """Test callback not triggered if value doesn't change."""
        mock_callback.reset_mock()
        current_value = slider.value
        
        # Update to same position (within threshold)
        slider._update_slider_position((int(current_value * 100), 5))
        
        # Callback should not be called for tiny changes
        assert mock_callback.call_count == 0
    
    def test_callback_called_on_value_change(self, slider, mock_callback):
        """Test callback is called when value changes."""
        mock_callback.reset_mock()
        
        slider._update_slider_position((75, 5))
        
        assert mock_callback.call_count == 1
        called_value = mock_callback.call_args[0][0]
        assert 0.74 < called_value < 0.76