import math
import constants
from game.casting.cast import Cast
from game.scripting.handle_game_over import HandleGameOver
from game.shared.point import Point

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
        _cast (Cast): For generating various casts
    """

    def __init__(self, keyboard_service, video_service, player1, player2, player1_score, player2_score, game_over_message):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            _keyboard_service (KeyboardService): An instance of KeyboardService.
            _video_service (VideoService): An instance of VideoService.
            _cast (Cast): The Cast of actors in the game
            _handle_game_over (HandleGameOver): An instance of HandleGameOver
            game_over (boolean): Declares if the game is over or not over
            winner (string): The winner of the game
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._cast = Cast()
        self.player1 = player1
        self.player2 = player2
        self._handle_game_over = HandleGameOver()
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.game_over_message = game_over_message
        
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
        player1_velocity = self._keyboard_service.get_direction('player1')
        player2_velocity = self._keyboard_service.get_direction('player2')
        self.player1.set_velocity(player1_velocity) 
        self.player2.set_velocity(player2_velocity)       

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with foods.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_actor("banners", 0)
        foods = cast.get_actors("foods")

        banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        self.player1.move_next(max_x, max_y)
        self.player2.move_next(max_x, max_y)

        # Player VS Food Collisions
        for food in foods:
            # Player 1
            player1_collision_distance = self.player1.get_radius() + food.get_radius()
            player1_position = self.player1.get_position()
            food_position = food.get_position()
            # Using pythagorean theorem to get distance
            distance = math.sqrt((player1_position.get_x() - food_position.get_x()) ** 2 + (player1_position.get_y() - food_position.get_y()) ** 2)
            if distance <= player1_collision_distance:
                self.player1.set_radius(self.player1.get_radius() + constants.RADIUS_INCREASE)
                cast.remove_actor("foods", food)
                self.player1_score.add_points(100)
            # Player 2
            player2_collision_distance = self.player2.get_radius() + food.get_radius()
            player2_position = self.player2.get_position()
            food_position = food.get_position()
            # Using pythagorean theorem to get distance
            distance = math.sqrt((player2_position.get_x() - food_position.get_x()) ** 2 + (player2_position.get_y() - food_position.get_y()) ** 2)
            if distance <= player2_collision_distance:
                self.player2.set_radius(self.player2.get_radius() + constants.RADIUS_INCREASE)
                cast.remove_actor("foods", food)
                self.player2_score.add_points(100)
        # End of PVE Collisions Logic
        
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
        player1 = cast.get_actor("players", 0)
        self._video_service.draw_player(player1)
        player2 = cast.get_actor("players", 1)
        self._video_service.draw_player(player2)
        self._video_service.draw_actor(self.player1_score)
        self._video_service.draw_actor(self.player2_score)
        game_over = ""
        if len(cast.get_list("foods")) == 0:
            game_over = self._handle_game_over._handle_game_over(self.player1_score, self.player2_score)
            self.player1.set_position(Point(300, 450))
            self.player2.set_position(Point(1600, 450))
            self._keyboard_service.disconnect_players()
        self._video_service.draw_actor(self.game_over_message)
        self._video_service.flush_buffer()
        self.player1_score.set_text(f"PLAYER 1 SCORE: {self.player1_score.get_points()}")
        self.player2_score.set_text(f"PLAYER 2 SCORE: {self.player2_score.get_points()}")
        self.game_over_message.set_text(game_over)    