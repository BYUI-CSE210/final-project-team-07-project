from game.casting.actor import Actor


class Score(Actor):
    """
    This is the score that will accumulate as you pick up either rocks or gems in the game "Greed."

    Attributes:
        _points (int): The points.
    """
    def __init__(self):
        super().__init__()
        self._score_display = ""
        self._points = 0
        self._font_size = 15

    def get_points(self):
        """gets the points in the game.
        
        Returns:
            _points (int): The current score.
        """
        return self._points

    def display_points(self, display):
        """Displays the points.

        Args: 
            _score_display (string): display the current score
        """
        return self._score_display

    def add_points(self, points):
        """Accumulates the points as you gather positive or negative points
        
        Args:
            _points (string): increase or decrease the current score
        """
        self._points += points
        self.set_text(f"Score: {self._points}")

    def set_font_size(self, font_size):
        """Updates the font size to the given one.
        
        Args:
            font_size (int): The given font size.
        """
        self._font_size = font_size