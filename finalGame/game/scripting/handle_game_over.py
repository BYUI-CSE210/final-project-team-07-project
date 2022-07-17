# A T T E N T I O N  * * * * * * * * * * * 
# THIS FILE IS CURRENTLY NOT WORKING AT ALL
# WE NEED TO FIX THIS FILE

from game.casting.cast import Cast
from game.casting.actor import Actor
from game.scripting.action import Action

class HandleGameOver(Action):
    """
    Checks if the Game is over or not & declares a winner or tie

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
        message (Actor): For declaring a winner or tie
        _player1_radius (int): the radius of player 1
        _player2_radius (int): the radius of player 2
        _cast (Cast): the cast of the message
        _remaining_food (int): the amount of remaining food
    """

    def __init__(self):
        self._is_game_over = False 
        self.message = Actor()
        self._cast = Cast()

    def execute(self, cast, script):
        """Executes the handle game over action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_game_over(self._cast)

    def _handle_game_over(self, player1_score, player2_score):
        """Shows the 'game over' message"""

        # if player1 is bigger, declare player1 as the winner
        if player1_score.get_points() > player2_score.get_points():
            self.message = "Player 1 Wins!"

        # if player2 is bigger, declare player2 as the winner
        if player2_score.get_points() > player1_score.get_points():
            self.message = "Player 2 Wins!"

        # if both players are the same size, declare a tie
        if player1_score.get_points() == player2_score.get_points():
            self.message = "Both Players are the same size! Tie Game!"

        return self.message
