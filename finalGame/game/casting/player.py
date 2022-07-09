from game.casting.actor import Actor
from pyray import draw_circle
from game.shared.color import Color
from game.shared.point import Point


class Player(Actor):
    def __init__(self):
        super().__init__()
        self._posx = 0
        self._posy = 0
        self._cradious = 0
        self._color = Color(255, 255, 255)


    def set_player(self, posx,posy,cradius,color):
        self._posx = posx
        self._posy = posy
        self._cradious = cradius
        self._color = color

    def get_player(self):

        return self._posx, self._posy,self._cradious,self._color