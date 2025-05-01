""" Grid.py 

Benjamin Bouie 

Cell, Grid, and Controller classes 

"""



from graphics import GraphWin, Point, Rectangle, Circle, Image

from piece import Piece # piece.py keeps getting overwritten to Piece.py and I can't figure out why 

from button import Button

from OthelloAI import *



class Cell(): 

    def __init__(self, center, win): 

        self.HEIGHT: int = 75 

        self.COLOR: str = "#009066"

        self.center: tuple(int,int) = center 

        self.occupied: bool = False

        self.resident = None

        self.win = win



        # Define a cell by its center and draw it to window

        p1 = Point(self.center[0] - (self.HEIGHT / 2) , self.center[1] + (self.HEIGHT / 2)) 

        p2 = Point(self.center[0] + (self.HEIGHT /  2) , self.center[1] - (self.HEIGHT / 2)) 

        self.cell = Rectangle(p1, p2)

        self.cell.setFill(self.COLOR)

        self.cell.draw(self.win)



    # mutators 

    def mark(self) -> None :    

        self.outerRing = Circle(Point(self.center[0], self.center[1]), self.HEIGHT - 40)

        self.outerRing.setOutline("#a0acb1") 

        self.innerRing = Circle(Point(self.center[0], self.center[1]), self.HEIGHT - 41)

        self.innerRing.setOutline("#a0acb1") 





        self.outerRing.draw(self.win)

        self.innerRing.draw(self.win)



    def unmark(self) -> None:

        self.outerRing.undraw()

        self.innerRing.undraw()



    def occupy(self, color) -> bool: 

        self.occupied = True

        self.resident = color

        return True



    def vacate(self) -> bool: 

        self.occupied = False

        return False



    # accessors

    def getCenter(self) -> tuple: 

        return (self.center[0], self.center[1])



    def getResident(self) -> str: 

        if self.occupied == True:

            return self.resident



    def open(self) -> bool:

        if self.occupied == False: 

            return True 

        return False



    def clicked(self, pt) -> bool: 

        """returns bool True if the button is active and Point pt is on the

        button; otherwise it returns False"""

        xPt = pt.getX()

        yPt = pt.getY()

        if self.center[0] - self.HEIGHT / 2 < xPt < self.center[0] + self.HEIGHT / 2: 

            if self.center[1] - self.HEIGHT / 2 < yPt < self.center[1] + self.HEIGHT / 2: 

                return True 

        return False





class Grid(): 

    def __init__(self, win): 

        self.playerPosition: dict[tuple, str] = { } 

        self.tiles: dict[object] = { }

        self.win = win 



        self._drawGrid()



    def _drawGrid(self) -> None:  

        "creates the grid with looping squares and assigns each to list"



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

        openTiles = [ ]

        for key, tile in self.tiles.items(): 

            if tile.occupied == False: openTiles.append(tile)

        return openTiles



    def getTiles(self) -> dict: 

        return self.tiles



    def getPosition(self) -> tuple:  

        return (self.playerPosition.getX(), self.playerPosition.getY())





class Controller():  

    """Holds all the data and owns all the piece classes"""

    def __init__(self, tiles, win): 

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



    def validMoves(self) -> tuple: 

        """Return the indices of the valid moves on the board and mark their tiles"""



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
        whiteSandwiches = []
        blackSandwiches = []
        directions = [1, -1, 8, -8, 7, -7, 9, -9]

        current_color = self.turn
        opponent_color = "white" if current_color == "black" else "black"

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
                    #piece.undraw()
                    #self.pieces.remove(piece)
                    break
            
            piece2.undraw()
            piece2.color = self.turn
            if piece2.color == 'white':
                piece2.path = "white-tile.png"
            elif piece2.color == 'black':
                piece2.path = "black-tile.png"
            piece2.image = Image(piece2.position, piece2.path)
            piece2.draw()
            
            #new = Piece(self.turn, self.tiles[tile].getCenter(), self.win, tile)
            #new.draw()
            #self.flip(tile)

        return self.blackMoves if current_color == "black" else self.whiteMoves


            

    def flip(self, tile) -> None: 

        """Visually add/remove pieces from the board"""

        moves = self.validMoves()

        blackMoves = moves[0]

        whiteMoves = moves[1]

        if tile in blackMoves and self.turn == "black": 

            old = self.tiles[tile].getResident()

            if old != None: old.undraw()

            new = Piece(self.turn, self.tiles[tile].getCenter(), self.win, tile)
            new.draw()


        elif tile in whiteMoves and self.turn == "white":  # same thing - make this into one method 

            old = self.tiles[tile].getResident()

            if old != None: old.undraw()

            new = Piece(self.turn, self.tiles[tile].getCenter(), self.win, tile)
            new.draw()


    def changeTurn(self) -> None: 

        # if self.turn == None: self.turn = "black"

        if self.turn == "black": self.turn = "white"

        elif self.turn == "white": self.turn = "black"



    # accessors 

    def getPieces(self) -> list: 

        return self.pieces 



    def position2Index(self, position: tuple) -> int: 

        """Converts a given position to a tile index on the board."""

        for key, value in self.tiles.items(): 

            if position == value.getCenter(): 

                return key





def convert(number):

    row = number // 8

    col = number - 8 * row

    return row, col



    

def get_best_move(board, valid_moves, color):

    moves = []

    for move in valid_moves:

        y, x = convert(move)

        moves.append((x,y))

        print(x, y)

        print(weighted_score(x, y, board, 4, color))

    return



def main():

    win = GraphWin("Othello", 1300,875)

    board = Grid(win)

    tiles = board.getTiles()

    setup = Controller(tiles, win)

    moves = setup.validMoves()

    pt = win.getMouse()

    print(tiles)

    for tile in tiles: 

        if setup.tiles[tile].clicked(pt): 

            print(f"tile {tile} was clicked")

    # for piece in setup.getPieces():

    #     print(piece.getX(), piece.getY(), piece.getColor())



    # get_best_move(setup.getPieces(), moves[0], "black")

    

    

if __name__ == "__main__":

    main()
