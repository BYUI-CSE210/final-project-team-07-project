from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

from operator import concat

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.

    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the other player, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False 

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)


    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        scores = cast.get_actors("scores")
        snakes = cast.get_actors("snakes")

        snake_1 = snakes[0].get_head()
        snake_2 = snakes[1].get_head()

        snake_1_segments = snakes[0].get_segments()
        snake_2_segments = snakes[1].get_segments()

        
        for segment in snake_1_segments:
            if snake_2.get_position().equals(segment.get_position()):
                self._is_game_over = True
                scores[1].add_points(1)
                

        for segment in snake_2_segments:
            if snake_1.get_position().equals(segment.get_position()):
                self._is_game_over = True
                scores[0].add_points(1)
                



    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            snakes = cast.get_actors("snakes")
            snake_1_segments = snakes[0].get_segments()
            snake_2_segments = snakes[1].get_segments()
            segments = concat(snake_1_segments, snake_2_segments)

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            for segment in segments:
                segment.set_color(constants.WHITE)
            for snake in snakes:
                snake.set_color(constants.WHITE)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)


            
