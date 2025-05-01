""" Grid.py 

Benjamin Bouie 

Cell, Grid, and Controller classes 

"""

from graphics import GraphWin, Point, Rectangle, Circle, Image
from piece import Piece # piece.py keeps getting overwritten to Piece.py and I can't figure out why 
from button import Button
from OthelloAI import *

class Cell(): 
    """
    Represents a single cell (square) on the Othello board.
    
    Each cell can be occupied by a piece and can be marked for
    indicating valid moves available to the player.
    """
    def __init__(self, center, win): 
        """
        Initialize a new cell at the specified center position.
        
        Args:
            center: (x,y) pixel coordinates for the center of the cell
            win: The GraphWin window to draw in
        """
        self.HEIGHT: int = 75 
        self.COLOR: str = "#009066"
        self.center: tuple(int,int) = center 
        self.occupied: bool = False
        self.resident = None
        self.win = win
        self.marked: bool = False

        # Define a cell by its center and draw it to window
        p1 = Point(self.center[0] - (self.HEIGHT / 2) , self.center[1] + (self.HEIGHT / 2)) 
        p2 = Point(self.center[0] + (self.HEIGHT /  2) , self.center[1] - (self.HEIGHT / 2)) 
        self.cell = Rectangle(p1, p2)
        self.cell.setFill(self.COLOR)
        self.cell.draw(self.win)

    # mutators 
    def mark(self) -> None :    
        """
        Mark this cell as a valid move by drawing circles around it.
        Only marks the cell if it's not already marked.
        """
        if self.marked == False:
            self.outerRing = Circle(Point(self.center[0], self.center[1]), self.HEIGHT - 40)
            self.outerRing.setOutline("#a0acb1") 
            self.innerRing = Circle(Point(self.center[0], self.center[1]), self.HEIGHT - 41)
            self.innerRing.setOutline("#a0acb1") 

            self.outerRing.draw(self.win)
            self.innerRing.draw(self.win)
            self.marked = True

    def unmark(self) -> None:
        """
        Remove the valid move marking from this cell.
        Only unmarks if the cell is currently marked.
        """
        if self.marked == True:
            self.outerRing.undraw()
            self.innerRing.undraw()
            self.marked = False

    def occupy(self, color) -> bool: 
        """
        Mark this cell as occupied by a piece of the specified color.
        
        Args:
            color: Color of the occupying piece ('black' or 'white')
            
        Returns:
            True to indicate successful occupation
        """
        self.occupied = True
        self.resident = color
        return True

    def vacate(self) -> bool: 
        """
        Mark this cell as unoccupied.
        
        Returns:
            False to indicate the cell is now unoccupied
        """
        self.occupied = False
        return False

    # accessors
    def getCenter(self) -> tuple: 
        """Return the (x,y) pixel coordinates of the cell's center."""
        return (self.center[0], self.center[1])

    def getResident(self) -> str: 
        """
        Return the color of the piece occupying this cell.
        
        Returns:
            Color of the resident piece, or None if unoccupied
        """
        if self.occupied == True:
            return self.resident

    def open(self) -> bool:
        """
        Check if this cell is unoccupied.
        
        Returns:
            True if the cell is unoccupied, False otherwise
        """
        if self.occupied == False: 
            return True 
        return False

    def clicked(self, pt) -> bool: 
        """
        Check if a point is within this cell.
        
        Args:
            pt: Point object representing the click location
            
        Returns:
            True if the point is inside this cell, False otherwise
        """
        xPt = pt.getX()
        yPt = pt.getY()
        if self.center[0] - self.HEIGHT / 2 < xPt < self.center[0] + self.HEIGHT / 2: 
            if self.center[1] - self.HEIGHT / 2 < yPt < self.center[1] + self.HEIGHT / 2: 
                return True 
        return False

class Grid(): 
    """
    Represents the 8x8 Othello game board.
    
    The grid consists of 64 cells arranged in an 8x8 grid.
    It manages the board itself but not the game pieces.
    """
    def __init__(self, win): 
        """
        Initialize a new Othello game board.
        
        Args:
            win: The GraphWin window to draw in
        """
        self.playerPosition: dict[tuple, str] = { } 
        self.tiles: dict[object] = { }
        self.win = win 

        self._drawGrid()

    def _drawGrid(self) -> None:  
        """
        Create the grid with 64 cells and draw the board markers.
        Each cell is indexed from 0-63 reading left to right, top to bottom.
        """
        horizontalCoords = 400
        verticalCoords = 100 
        cellIndex = 0 

        # draw the squares on the board 
        for row in range(8): 
            verticalCoords += 75
            for tile in range(8):
                cell = Cell((horizontalCoords,verticalCoords), self.win)
                self.tiles[cellIndex] = cell
                cellIndex += 1
                horizontalCoords += 75 
                if horizontalCoords >= 1000: 
                    horizontalCoords = 400

        # draw the dots in the middle of the square 
        p1 = Circle(Point(513,288), 4)
        p2 = Circle(Point(813,288), 4)
        p3 = Circle(Point(513,588), 4)
        p4 = Circle(Point(813, 588), 4)
        p1.setFill("black")
        p2.setFill("black")
        p3.setFill("black")
        p4.setFill("black")
        p1.draw(self.win)
        p2.draw(self.win)
        p3.draw(self.win)
        p4.draw(self.win)

    # accessors 
    def getOpenTiles(self) -> list: 
        """
        Get a list of all unoccupied cells.
        
        Returns:
            List of all Cell objects that are currently unoccupied
        """
        openTiles = [ ]
        for key, tile in self.tiles.items(): 
            if tile.occupied == False: openTiles.append(tile)
        return openTiles

    def getTiles(self) -> dict: 
        """
        Get the dictionary of all cells on the board.
        
        Returns:
            Dictionary mapping position indices (0-63) to Cell objects
        """
        return self.tiles

    def getPosition(self) -> tuple:  
        """
        Get the player position. (Currently unused)
        
        Returns:
            Tuple representing the player position
        """
        return (self.playerPosition.getX(), self.playerPosition.getY())

class Controller():  
    """
    Controls the game logic and manages pieces on the board.
    
    The Controller handles game state, valid move detection, piece flipping,
    and turn management for the Othello game.
    """
    def __init__(self, tiles, win): 
        """
        Initialize the game controller with the starting board setup.
        
        Args:
            tiles: Dictionary of Cell objects representing the board
            win: The GraphWin window to draw in
        """
        # starting setup for the pieces 
        piece1 = Piece('white', (625,400), win, 27)
        piece2 = Piece('black', (700,400), win, 28)
        piece3 = Piece('black', (625,475), win, 35)
        piece4 = Piece('white', (700,475), win, 36)
        piece1.draw()
        piece2.draw()
        piece3.draw()
        piece4.draw()

        self.pieces = [piece1, piece2, piece3, piece4]
        self.blackPieces = [ ]
        self.whitePieces = [ ]
        self.turn: str = None
        self.win = win 

        for piece in self.pieces: 
            if piece.getColor() == 'black': 
                self.blackPieces.append(piece)
            elif piece.getColor() == 'white': 
                self.whitePieces.append(piece)

        self.tiles = tiles 
        for piece in self.pieces: 
            cell = self.position2Index(piece.getPosition())
            self.tiles[cell].occupy(piece.getColor())

    def unmarkall(self) -> None:
        """Remove valid move indicators from all cells on the board."""
        for tile in self.tiles:
            self.tiles[tile].unmark()

    def validMoves(self) -> tuple: 
        """
        Find and mark all valid moves for both players.
        
        Returns:
            Tuple of (valid black moves, valid white moves) as lists of position indices
        """
        directions = [1,-1,8,-8,7,-7,9,-9]
        self.blackMoves = [ ]
        self.whiteMoves = [ ]
        self.blackFutureMoves = [ ]

        for piece in self.blackPieces: 
            i = 0
            pieceColor = piece.getColor() 
            for direction in directions: 
                index = self.position2Index(piece.getPosition())
                while True:
                    index += directions[i] 

                    if index % 8 == 7: break 
                    if (index - 1) % 8 == 0: break 
                    if index < 0 or index > 63: break
                    
                    currentTile = self.tiles[index]
                    previousTile = self.tiles[index - directions[i]] 

                    if currentTile.open() and pieceColor != previousTile.getResident(): 
                        if not previousTile.open():
                            currentTile.mark() 
                            self.blackMoves.append(index)
                        break 
                i += 1

        for piece in self.whitePieces:  # !!!! must be rewritten to be more efficient 
            i = 0
            pieceColor = piece.getColor() 
            for element in directions: 
                index = self.position2Index(piece.getPosition())
                while True:
                    index += directions[i] 

                    if index % 8 == 7: break 
                    if (index - 1) % 8 == 0: break 
                    if index < 0 or index > 63: break
                    
                    currentTile = self.tiles[index]
                    previousTile = self.tiles[index - directions[i]] 

                    if currentTile.open() and pieceColor != previousTile.getResident(): 
                        if not previousTile.open():
                            self.whiteMoves.append(index)
                        break 
                i += 1

        return (self.blackMoves, self.whiteMoves) 

    def getSandwiches(self, tile):
        """
        Find and flip all pieces that would be captured by placing a piece at the specified position.
        
        Args:
            tile: Board position index (0-63) where the piece is placed
            
        Returns:
            List of valid moves for the current player
        """
        whiteSandwiches = []
        blackSandwiches = []
        directions = [1, -1, 8, -8, 7, -7, 9, -9]

        current_color = self.turn
        opponent_color = "white" if current_color == "black" else "black"

        # Check in all 8 directions for opponent pieces to capture
        for direction in directions:
            index = tile + direction
            path = []

            while 0 <= index < 64:
                # Stop if we're wrapping horizontally (left/right edge)
                if direction in [1, -1, 9, -7] and index % 8 == 0 and direction in [-1, 7]:
                    break
                if direction in [1, -1, 7, -9] and index % 8 == 7 and direction in [1, -9]:
                    break

                current_tile = self.tiles[index]

                if current_tile.open():
                    break
                elif current_tile.getResident() == opponent_color:
                    path.append(current_tile)
                elif current_tile.getResident() == current_color:
                    if current_color == "black":
                        blackSandwiches.extend(path)
                    else:
                        whiteSandwiches.extend(path)
                    break
                else:
                    break

                index += direction

        # Flip opponent tiles
        current_sandwiches = blackSandwiches
        if current_color == "white" :
            current_sandwiches =   whiteSandwiches
        for tile in current_sandwiches:
            x = tile.getCenter()[0]
            y = tile.getCenter()[1]
            xx = (x - 400) // 75
            yy = (y - 175) // 75
            print("sandwich:", xx, yy)
            tile = yy * 8 + xx
            
            piece2 = None
            for piece in self.pieces:
                if piece.pos == tile:
                    piece2 = piece
                    break
            
            piece2.undraw()
            piece2.color = self.turn
            self.tiles[tile].occupy(self.turn)  
            if piece2.color == 'white':
                piece2.path = "white-tile.png"
            elif piece2.color == 'black':
                piece2.path = "black-tile.png"
            piece2.image = Image(piece2.position, piece2.path)
            piece2.draw()

        return self.blackMoves if current_color == "black" else self.whiteMoves

    def flip(self, tile) -> None: 
        """
        Add a new piece at the specified position.
        
        Args:
            tile: Board position index (0-63) where to place the new piece
        """
        new = Piece(self.turn, self.tiles[tile].getCenter(), self.win, tile)
        self.pieces.append(new)              
        new.draw()

    def flip2(self, tile) -> None: 
        """
        Find and flip pieces captured by placing a piece at the specified position.
        
        Args:
            tile: Board position index (0-63) where the new piece is placed
        """
        directions = [1, -1, 8, -8, 7, -7, 9, -9]
        current_color = self.turn
        opponent_color = "white" if current_color == "black" else "black"

        for direction in directions:
            to_flip = []
            index = tile
            
            while True:
                index += direction
                
                # Check for board boundaries and wrapping
                if index < 0 or index >= 64:
                    break
                if direction in [1, 9, -7] and index % 8 == 0:
                    break
                if direction in [-1, -9, 7] and index % 8 == 7:
                    break
                
                if not self.tiles[index].open():
                    if self.tiles[index].getResident() == opponent_color:
                        to_flip.append(index)
                    elif self.tiles[index].getResident() == current_color and to_flip:
                        # Found a piece of our color after opponent pieces - flip them all
                        for flip_index in to_flip:
                            flip_piece = None
                            for piece in self.pieces:
                                if piece.pos == flip_index:
                                    flip_piece = piece
                                    break
                            
                            if flip_piece:
                                flip_piece.flipColor()
                                self.tiles[flip_index].occupy(current_color)
                        break
                    else:
                        # Found a piece of our color with no opponent pieces in between - invalid direction
                        break
                else:
                    # Found an empty space - invalid direction
                    break
                
    def changeTurn(self) -> None: 
        """
        Switch the current player's turn.
        """
        if self.turn == None or self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"
        print(f"Changed turn to {self.turn}")

    def getPieces(self) -> list: 
        """
        Get all pieces currently on the board.
        
        Returns:
            List of all Piece objects on the board
        """
        return self.pieces

    def position2Index(self, position: tuple) -> int: 
        """
        Convert pixel coordinates to a board position index.
        
        Args:
            position: Tuple of (x,y) pixel coordinates
            
        Returns:
            Board position index (0-63)
        """
        y = (position[1] - 175) // 75 
        x = (position[0] - 400) // 75 
        index = (y * 8) + x 
        return index

def convert(number):
    """
    Convert a board position index to row and column coordinates.
    
    Args:
        number: Board position index (0-63)
        
    Returns:
        Tuple of (row, column)
    """
    row = number // 8
    col = number - 8 * row
    return row, col

def oppositeColor(color):
    """
    Get the opposite color of the given color.
    
    Args:
        color: 'black' or 'white'
        
    Returns:
        The opposite color ('white' if input is 'black', 'black' if input is 'white')
    """
    if color == "black": return "white"
    elif color == "white": return "black"



def main():
    """
    Run a test instance of the Othello grid and controller.
    
    This function is not used in the main game loop but could be used for testing.
    """
    win = GraphWin("Othello", 1300,875)
    board = Grid(win)
    tiles = board.getTiles()
    controller = Controller(tiles, win)

if __name__ == "__main__": main()
