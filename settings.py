
class Settings:
    """
    Stores all configurable settings for the Vibe music player UI.

    This class centralizes color choices, screen dimensions, and slider
    appearance settings so they can be reused across multiple modules.
    """

    def __init__(self):
        """
        Initialize default settings for screen size, colors, and slider styling.
        """

        #Screen settings
        #main menu
        self.screen_colour = (200,200,200)
        self.screen_height = 700
        self.screen_width = 1200
    
        
        #options menu 
        self.screen_op_height = 700
        self.screen_op_width = 335
        self.screen_colour = (170, 170, 170)

        #slider settings
        self.slider_knob_color = (50,50,50)
        self.slider_bg_color = (100, 100, 100)
        self.slider_filled_color = (255, 255, 255)



