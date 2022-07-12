import os
import random

from pyray import draw_circle

from game.casting.actor import Actor
from game.casting.player import Player
from game.casting.artifact import Artifact
from game.casting.cast import Cast

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point


FRAME_RATE = 12
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 15
COLS = 60
ROWS = 40
CAPTION = "Agar.io"
WHITE = Color(255, 255, 255)
DEFAULT_ARTIFACTS = 40


def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the blob
    x = int(MAX_X / 2)
    y = int(MAX_Y / 2)
    position = Point(x, y)

    #CREATING THE PLAYER 1
    player1 = Player()
    player1.set_player(x,y,50,WHITE)
    player1.set_color(WHITE)
    player1.set_position(position)
    cast.add_actor("player1", player1)

    #PLAYER 2

     # Position for Player 2
    x2 = int(MAX_X / 2 + 200)
    y2 = int(MAX_Y / 2)
    position2 = Point(x2, y2)
     #Creating a Second Player
    player2 = Player()
    player2.set_player(x,y,20,WHITE)
    player2.set_color(WHITE)
    player2.set_position(position2)
    cast.add_actor("player2", player2)

    #create the artifacts

    for n in range(DEFAULT_ARTIFACTS):
        text = chr(random.randint(33, 126))

        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        #THE FOOD
        artifact = Artifact()
        artifact.set_text(text)
        artifact.set_color(color)
        artifact.set_position(position)
        cast.add_actor("artifacts", artifact)
    
    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()