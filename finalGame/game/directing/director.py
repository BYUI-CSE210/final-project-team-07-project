import math
import constants
from game.casting.cast import Cast
from game.scripting.handle_game_over import HandleGameOver

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
        _cast (Cast): For generating various casts
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._cast = Cast()
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        player1 = cast.get_first_actor("player1")
        player2 = cast.get_first_actor("player2")
        player1_velocity = self._keyboard_service.get_direction('player1')
        player2_velocity = self._keyboard_service.get_direction('player2')
        player1.set_velocity(player1_velocity) 
        player2.set_velocity(player2_velocity)       

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with foods.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        player1 = cast.get_first_actor("player1")
        player2 = cast.get_first_actor("player2")
        foods = cast.get_actors("foods")

        banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        player1.move_next(max_x, max_y)
        player2.move_next(max_x, max_y)

        # check if a player collides with food
        for food in foods:
            player1_collision_distance = player1.get_radius() + food.get_radius()
            player1_position = player1.get_position()
            food_position = food.get_position()
            #Using pythagorean therom to get distance
            distance = math.sqrt((player1_position.get_x() - food_position.get_x()) ** 2 + (player1_position.get_y() - food_position.get_y()) ** 2)
            if distance <= player1_collision_distance:
                player1.set_radius(player1.get_radius() + constants.RADIUS_INCREASE)
                cast.remove_actor("foods", food)
            # player 2
            player2_collision_distance = player2.get_radius() + food.get_radius()
            player2_position = player2.get_position()
            food_position = food.get_position()
            #Using pythagorean therom to get distance
            distance = math.sqrt((player2_position.get_x() - food_position.get_x()) ** 2 + (player2_position.get_y() - food_position.get_y()) ** 2)
            if distance <= player2_collision_distance:
                player2.set_radius(player2.get_radius() + constants.RADIUS_INCREASE)
                cast.remove_actor("foods", food)
            remaining_food = len(cast.get_actors("foods"))
            player1_radius = player1.get_radius()
            player2_radius = player2.get_radius()
            _handle_game_over = HandleGameOver(player1_radius, player2_radius, remaining_food)
            _handle_game_over._handle_game_over(self._cast)
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        food = cast.get_actors("foods")
        self._video_service.draw_players(food)
        banners = cast.get_actors("banner")
        self._video_service.draw_actors(banners) 
        player1 = cast.get_first_actor("player1")
        self._video_service.draw_player(player1)
        player2 = cast.get_first_actor("player2")
        self._video_service.draw_player(player2)
        self._video_service.flush_buffer()
        