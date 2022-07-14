import math
import constants
from game.casting.cast import Cast
from game.scripting.handle_game_over import HandleGameOver
from game.scripting.handle_collisions import HandleCollisions
class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
        _cast (Cast): For generating various casts
    """

    def __init__(self, keyboard_service, video_service, player1, player2):
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
        self._handle_collisions = HandleCollisions(self.player1, self.player2)
        
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

        # This block works fine but I want to move it over to handle_collisions.py eventually
        # Delete this collisions logicblock when handle_collisions.py file is working properly
        # Collisions Logic
        # PVE Collisions
        for food in foods:
            # Player 1
            player1_collision_distance = self.player1.get_radius() + food.get_radius()
            player1_position = self.player1.get_position()
            food_position = food.get_position()
            #Using pythagorean therom to get distance
            distance = math.sqrt((player1_position.get_x() - food_position.get_x()) ** 2 + (player1_position.get_y() - food_position.get_y()) ** 2)
            if distance <= player1_collision_distance:
                self.player1.set_radius(self.player1.get_radius() + constants.RADIUS_INCREASE)
                cast.remove_actor("foods", food)
            # Player 2
            player2_collision_distance = self.player2.get_radius() + food.get_radius()
            player2_position = self.player2.get_position()
            food_position = food.get_position()
            #Using pythagorean therom to get distance
            distance = math.sqrt((player2_position.get_x() - food_position.get_x()) ** 2 + (player2_position.get_y() - food_position.get_y()) ** 2)
            if distance <= player2_collision_distance:
                self.player2.set_radius(self.player2.get_radius() + constants.RADIUS_INCREASE)
                cast.remove_actor("foods", food)
        # End of PVE Collisions Logic
        # PVP Collisions Logic:
        # these half_radius variables require the players to get closer to each other to fight which makes the game more competitive
        player1_half_radius = self.player1.get_radius() / 2
        player2_half_radius = self.player2.get_radius() / 2
        pvp_collision_distance = player1_half_radius + player2_half_radius
        player1_position = self.player1.get_position()
        player2_position = self.player2.get_position()
        pvp_distance = math.sqrt((player1_position.get_x() - player2_position.get_x()) ** 2 + (player1_position.get_y() - player2_position.get_y()) ** 2)
        if pvp_distance <= pvp_collision_distance:
            # if player 1 is bigger than player 2, remove player 2 & declare player 1 as the winner
            if self.player1.get_radius() > self.player2.get_radius():
                # set opacity of player2 to 0 to make it invisible. This actually works but remove_actor doesn't work & I haven't been able to track down why
                # self.player2.set_color(constants.INVISBLE_OPACITY)
                self._cast.remove_actor('players', self.player2)
                # this isn't recognizing when a player eats the other player to end the game & I haven't been able to track down why
                self._handle_game_over._handle_game_over(self._cast, "player1")

            # if player 2 is bigger than player 2, remove player 1 & declare player 2 as the winner
            if self.player1.get_radius() < self.player2.get_radius():
                # set opacity of player1 to 0 to make it invisible. This actually works but remove_actor doesn't work & I haven't been able to track down why
                # self.player1.set_color(constants.INVISBLE_OPACITY)
                self._cast.remove_actor('players', self.player1)
                # this isn't recognizing when a player eats the other player to end the game & I haven't been able to track down why
                self._handle_game_over._handle_game_over(self._cast, "player2")

            # if both players are the same size AND there is no more food, then declare a tie
            if self.player1.get_radius() < self.player2.get_radius() and len(foods) == 0:
                # this isn't recognizing when a player eats the other player to end the game & I haven't been able to track down why
                self._handle_game_over._handle_game_over(self._cast, "tie")
        # END OF PVP COLLISIONS LOGIC

        # This following Collisions BLock is in progress. It will replace the above collisions block if we get it working. The current issue with the below code is that it keeps increasing the radius of the circle forever so we need to figure out how to only increase the radius once per food collected.

        # player vs food collisions
        # for food in foods:
            # # Player 1
            # self._handle_collisions._pve_collisions(self.player1, food)
            # # Player 2
            # self._handle_collisions._pve_collisions(self.player2, food)
        # player vs player collisions
        # self._handle_collisions._pvp_collisions()
        
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
        self._video_service.flush_buffer()
        