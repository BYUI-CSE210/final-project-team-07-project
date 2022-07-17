import pyray
from game.shared.point import Point
from game.casting.cast import Cast


class KeyboardService:
    """Detects player input. 
    
    The responsibility of a KeyboardService is to detect player key presses and translate them into 
    a point representing a direction.

    Attributes:
        cell_size (int): For scaling directional input to a grid.
    """

    def __init__(self, cell_size = 1):
        """Constructs a new KeyboardService using the specified cell size.
        
        Args:
            cell_size (int): The size of a cell in the display grid.
        """
        self._cell_size = cell_size

    def get_direction(self, player):
        """Gets the selected direction based on the currently pressed keys.

        Returns:
            Point: The selected direction.
        """
        directional_x = 0
        directional_y = 0
        if player == 'player1':
            if pyray.is_key_down(pyray.KEY_A):
                directional_x = -1
            
            if pyray.is_key_down(pyray.KEY_D):
                directional_x = 1
            
            if pyray.is_key_down(pyray.KEY_W):
                directional_y = -1
            
            if pyray.is_key_down(pyray.KEY_S):
                directional_y = 1
                
        if player == 'player2':
            if pyray.is_key_down(pyray.KEY_LEFT):
                directional_x = -1
            
            if pyray.is_key_down(pyray.KEY_RIGHT):
                directional_x = 1
            
            if pyray.is_key_down(pyray.KEY_UP):
                directional_y = -1
            
            if pyray.is_key_down(pyray.KEY_DOWN):
                directional_y = 1

        direction = Point(directional_x, directional_y)
        direction = direction.scale(self._cell_size)
        
        return direction

    def disconnect_players(self):
        """When the game is over, disconnect both players from keyboard input so they can longer move"""
        directional_x = 0
        directional_y = 0
        
        if pyray.is_key_down(pyray.KEY_A):
            directional_x = 0
            
        if pyray.is_key_down(pyray.KEY_D):
            directional_x = 0
        
        if pyray.is_key_down(pyray.KEY_W):
            directional_y = 0
        
        if pyray.is_key_down(pyray.KEY_S):
            directional_y = 0

        if pyray.is_key_down(pyray.KEY_LEFT):
            directional_x = 0
        
        if pyray.is_key_down(pyray.KEY_RIGHT):
            directional_x = 0
        
        if pyray.is_key_down(pyray.KEY_UP):
            directional_y = 0
        
        if pyray.is_key_down(pyray.KEY_DOWN):
            directional_y = 0

        direction = Point(directional_x, directional_y)
        direction = direction.scale(self._cell_size)
        
        return direction