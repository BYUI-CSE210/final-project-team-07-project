# STILL IN PROGRESS

import math
import constants
from game.casting.cast import Cast
from game.scripting.handle_game_over import HandleGameOver

class HandleCollisions():
    """Handle the Collisions for the Players and Food

    Attributes:
        _cast (Cast): The cast of actors in the game
        _player1 (Player): An instance of Player
        _player2 (Player): An instance of Player
        _foods (list): A list of the food actors
    """
    def __init__(self, player1, player2):
        self._cast = Cast()
        self._player1 = player1
        self._player2 = player2
        self._handle_game_over = HandleGameOver()
        self.foods_list = self._cast.get_actors("foods")

    def _pve_collisions(self, food):
        """Handle the collisions of the Player and the Food"""
        player1_collision_distance = self._player1.get_radius() + food.get_radius()
        player1_position = self._player1.get_position()
        food_position = food.get_position()
        #Using pythagorean therom to get distance
        distance = math.sqrt((player1_position.get_x() - food_position.get_x()) ** 2 + (player1_position.get_y() - food_position.get_y()) ** 2)
        if distance <= player1_collision_distance:
            self._player1.set_radius(self._player1.get_radius() + constants.RADIUS_INCREASE)
            self._cast.remove_actor("foods", food)
        # player 2
        player2_collision_distance = self._player2.get_radius() + food.get_radius()
        player2_position = self._player2.get_position()
        food_position = food.get_position()
        #Using pythagorean therom to get distance
        distance = math.sqrt((player2_position.get_x() - food_position.get_x()) ** 2 + (player2_position.get_y() - food_position.get_y()) ** 2)
        if distance <= player2_collision_distance:
            self._player2.set_radius(self._player2.get_radius() + constants.RADIUS_INCREASE)
            self._cast.remove_actor("foods", food)

    def _pvp_collisions(self):
        """Handle the collisions of Player vs Player"""
        # these half_radius variables require the players to get closer to each other to fight which makes the game more competitive
        player1_half_radius = self._player1.get_radius() / 2
        player2_half_radius = self._player2.get_radius() / 2
        # PVP Collision Logic:
        pvp_collision_distance = player1_half_radius + player2_half_radius
        player1_position = self._player1.get_position()
        player2_position = self._player2.get_position()
        pvp_distance = math.sqrt((player1_position.get_x() - player2_position.get_x()) ** 2 + (player1_position.get_y() - player2_position.get_y()) ** 2)

        if pvp_distance <= pvp_collision_distance:
            # if player 1 is bigger than player 2, remove player 2 & declare player 1 as the winner
            if self._player1.get_radius() > self._player2.get_radius():
                # set opacity of player2 to 0 to make it invisible. This works better than just removing player2
                self._player2.set_color(constants.INVISBLE_OPACITY)
                # declare game_over(Arg 2) as True and winner(Arg 3) as "player1"
                self._handle_game_over._handle_game_over(self._cast, True, "player1")

            # if player 2 is bigger than player 2, remove player 1 & declare player 2 as the winner
            if self._player1.get_radius() < self._player2.get_radius():
                # set opacity of player1 to 0 to make it invisible. This works better than just removing player1
                self._player1.set_color(constants.INVISBLE_OPACITY)
                # declare game_over(Arg 2) as True and winner(Arg 3) as "player1"
                self._handle_game_over._handle_game_over(self._cast, True, "player2")

            # if both players are the same size AND there is no more food, then declare a tie
            if self._player1.get_radius() < self._player2.get_radius() and len(self.foods_list) == 0:
                # declare game_over(Arg 2) as True and winner(Arg 3) as "player1"
                self._handle_game_over._handle_game_over(self._cast, True, "tie")