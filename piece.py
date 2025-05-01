""" piece.py 
Benjamin Bouie 
Piece class
Keeps getting renamed to `Piece.py` and I can't find the swapfile
"""

from graphics import Point, Image 

class Piece:
    def __init__(self, color: str, position, win, pos) -> None:
        # Display attributes
        self.color = color
        self.path = None
        self.win = win
        self.pos = pos
        self.y, self.x = self.convert(pos)
        if self.color == 'white': 
            self.path = "white-tile.png"
        elif self.color == 'black': 
            self.path = "black-tile.png"

        # Gameplay attributes
        self.position = Point(position[0], position[1]) 
        self.image = Image(self.position, self.path)

    def draw(self):
        self.image.draw(self.win)
        
    def undraw(self):
        self.image.undraw()

    # accessors
    def convert(self, number):
        row = number // 8
        col = number - 8 * row
        return row, col

    def grid_to_board_x(self, coord):
        return (coord - 400) // 75

    def grid_to_board_y(self, coord):
        return (coord - 175) // 75

    def coord_to_pos(self, x, y):
        return 8*y + x
    
    def getColor(self) -> str: 
        return self.color

    def getPosition(self) -> tuple:  
        return (self.position.getX(), self.position.getY())

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def flipColor(self):
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
