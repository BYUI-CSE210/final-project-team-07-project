# A T T E N T I O N  * * * * * * * * * * * 
# THIS FILE IS CURRENTLY NOT WORKING AT ALL
# WE NEED TO FIX THIS FILE

from game.casting.cast import Cast
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
import constants

class HandleGameOver(Action):
    """
    Checks if the Game is over or not & declares a winner or tie

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
        _message (Actor): For declaring a winner or tie
        _player1_radius (int): the radius of player 1
        _player2_radius (int): the radius of player 2
        _cast (Cast): the cast of the message
        _remaining_food (int): the amount of remaining food
    """

    def __init__(self):
        self._is_game_over = False 
        self._message = Actor()
        self._cast = Cast()

    def execute(self, cast, script):
        """Executes the handle game over action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_game_over(self._cast)

    def _handle_game_over(self, cast, winner):
        """Shows the 'game over' message & removes any remaining food."""

        # delete any remaining food
        cast.clear_list("foods")

        x = int(constants.MAX_X / 2)
        y = int(constants.MAX_Y / 2)
        position = Point(x, y)

        self._message.set_font_size(20)
        self._message.set_color(constants.RED)
        self._message.set_position(position)
        cast.add_actor("messages", self._message)

        # if player1 is bigger, declare player1 as the winner
        if winner == "player1":
            self._message.set_text("Player 1 Wins!")

        # if player2 is bigger, declare player2 as the winner
        if winner == "player2":
            self._message.set_text("Player 2 Wins!")

        # if both players are the same size, declare a tie
        if winner.lower() == 'tie':
            self._message.set_text("Both Players are the same size! Tie Game!")
