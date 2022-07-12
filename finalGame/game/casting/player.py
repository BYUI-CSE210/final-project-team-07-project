from game.casting.actor import Actor
from game.shared.color import Color

class Player(Actor):
    def __init__(self):
        super().__init__()
        self._radious = 0
        self._color = Color(255, 255, 255)
    
    def get_radius(self):
        return self._radius 

    
    def set_radius(self, radius):
        self._radius = radius