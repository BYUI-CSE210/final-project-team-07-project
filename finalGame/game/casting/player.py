from game.casting.actor import Actor
from game.shared.color import Color

class Player(Actor):
    """ One of the players in the game

    Attributes: 
        radius (int): the radius of the player
        color (Color): the color of the player
    """
    def __init__(self):
        super().__init__()
        self._radius = 0
        self._color = Color(255, 255, 255)
    
    def get_radius(self):
        """Get the radius of the player's circle"""
        return self._radius 
    
    def set_radius(self, radius):
        """Set the radius of the player's circle to a given radius"""
        self._radius = radius