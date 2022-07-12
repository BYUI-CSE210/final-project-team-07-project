import os
import random

from pyray import draw_circle

# Casting
from game.casting.actor import Actor
from game.casting.player import Player
from game.casting.cast import Cast

# Director
from game.directing.director import Director

# Services
from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

# Scripting

# Shared
from game.shared.color import Color
from game.shared.point import Point

import constants

def main():
    """Play the entire game"""
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_color(constants.WHITE)
    banner.set_position(Point(constants.CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the blob
    x = int(constants.MAX_X / 2)
    y = int(constants.MAX_Y / 2)
    position = Point(x, y)

    #CREATING THE PLAYER 1
    player1 = Player()
    player1.set_radius(20)
    player1.set_color(constants.WHITE)
    player1.set_position(position)
    cast.add_actor("player1", player1)

    #PLAYER 2

     # Position for Player 2
    x2 = int(constants.MAX_X / 2 + 200)
    y2 = int(constants.MAX_Y / 2)
    position2 = Point(x2, y2)
     #Creating a Second Player
    player2 = Player()
    player2.set_radius(20)
    player2.set_color(constants.WHITE)
    player2.set_position(position2)
    cast.add_actor("player2", player2)

    #create the food

    for n in range(constants.AMOUNT_OF_FOOD):

        x = random.randint(1, constants.COLUMNS - 1)
        y = random.randint(1, constants.ROWS - 1)
        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        radius = 20
        
        #THE FOOD
        food = Player()
        food.set_color(color)
        food.set_position(position)
        food.set_radius(radius)
        cast.add_actor("foods", food)
    
    # start the game
    keyboard_service = KeyboardService(constants.CELL_SIZE)
    video_service = VideoService(constants.CAPTION, constants.MAX_X, constants.MAX_Y, constants.CELL_SIZE, constants.FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()