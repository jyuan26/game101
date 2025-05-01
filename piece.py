""" piece.py 
Benjamin Bouie 
Piece class
Keeps getting renamed to `Piece.py` and I can't find the swapfile
"""

from graphics import Point, Image 

class Piece:
    """
    Represents a game piece (disc) in Othello.
    
    This class manages both the visual representation and logical properties
    of an Othello disc, including its color, position, and methods to flip it.
    """
    def __init__(self, color: str, position, win, pos) -> None:
        """
        Initialize a new Othello piece.
        
        Args:
            color: The color of the piece ('white' or 'black')
            position: The (x,y) pixel coordinates for drawing
            win: The GraphWin window to draw in
            pos: The logical board position (0-63)
        """
        # Display attributes
        self.color = color
        self.path = None
        self.win = win
        self.pos = pos
        self.y, self.x = self.convert(pos)  # Convert board position to row, col
        if self.color == 'white': 
            self.path = "white-tile.png"
        elif self.color == 'black': 
            self.path = "black-tile.png"

        # Gameplay attributes
        self.position = Point(position[0], position[1]) 
        self.image = Image(self.position, self.path)

    def draw(self):
        """Draw the piece on the game window."""
        self.image.draw(self.win)
        
    def undraw(self):
        """Remove the piece from the game window."""
        self.image.undraw()

    # accessors
    def convert(self, number):
        """
        Convert a board position (0-63) to row and column coordinates.
        
        Args:
            number: Board position from 0-63
            
        Returns:
            Tuple of (row, column)
        """
        row = number // 8
        col = number - 8 * row
        return row, col

    def grid_to_board_x(self, coord):
        """
        Convert a pixel x-coordinate to a board column.
        
        Args:
            coord: Pixel x-coordinate
            
        Returns:
            Board column (0-7)
        """
        return (coord - 400) // 75

    def grid_to_board_y(self, coord):
        """
        Convert a pixel y-coordinate to a board row.
        
        Args:
            coord: Pixel y-coordinate
            
        Returns:
            Board row (0-7)
        """
        return (coord - 175) // 75

    def coord_to_pos(self, x, y):
        """
        Convert board coordinates to a board position.
        
        Args:
            x: Board column (0-7)
            y: Board row (0-7)
            
        Returns:
            Board position (0-63)
        """
        return 8*y + x
    
    def getColor(self) -> str: 
        """Return the current color of the piece."""
        return self.color

    def getPosition(self) -> tuple:  
        """Return the pixel coordinates of the piece."""
        return (self.position.getX(), self.position.getY())

    def getX(self):
        """Return the column (0-7) of the piece on the board."""
        return self.x

    def getY(self):
        """Return the row (0-7) of the piece on the board."""
        return self.y

    def flipColor(self):
        """
        Flip the piece to the opposite color and redraw it.
        This is used when a piece is captured during gameplay.
        """
        if self.color == "white":
            self.color = 'black'
            self.path = "black-tile.png"
        else:
            self.color = 'white'
            self.path = "white-tile.png"
            
        self.image.undraw()
        self.image = Image(self.position, self.path)
        self.image.draw(self.win)

    def flipColorNoChange(self):
        """
        Flip the piece color in memory without redrawing.
        This is useful for simulating moves without visual changes.
        """
        if self.color == "white":
            self.color = 'black'
            self.path = "black-tile.png"
        else:
            self.color = 'white'
            self.path = "white-tile.png"

    
# def validMove(self, tile: tuple) -> bool: 
#     """
#     determine if the piece can capture a given square 
#     there are two conditions to determine whether a piece can capture a square: 
#         1. Is there an uninterrupted line of squares of the same color adjacent to the piece? 
#         2. Are the pieces color's opposite to the `self`?
#     -------
#     args: 
#         - tile (the method checks one tile at a time)
#         --> tile.occupied 
#     return: bool 
#     """
#
#     if tile.occupied
#
#
#         get the list of occupied tiles 
        
    #
    # for piece in self.pieces: 
    #     for tile in self.tiles: 
    #         if (tile + 1).occupy() == True: 
    #             adjacentSquares.append(tile + 1)
    #         if (piece.getPosition() - 1).occupy() == True
    #             adjacentSquares.append(tile - 1)
    #         if (piece.getPosition() - 8).occupy() == True
    #             adjacentSquares.append(tile - 8)
    #         if (piece.getPosition() + 8 ).occupy() == True
    #             adjacentSquares.append(tile + 8)
    #
    # return adjacentSquares

# def flip(self) -> list: 
#     """flip the piece if it is surrounded by two pieces of the opposite color"""
#     self._surround()
#     for piece in self.pieces: 
#         if <CONDITION>: 
#             piece.flipColor()
#         elif <CONDITION> 
#             piece.flipColor()
#
#     return self.pieces

# TO DO 
# def main(): 
#     piece1 = Piece(black)
