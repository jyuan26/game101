"""
Othello.py 
Benjamin Bouie 
Othello main 
"""

from piece import Piece 
from grid import Cell, Grid, Controller
from graphics import GraphWin, Point, Text
from button import Button 
from OthelloAI import *

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
    if color == "black":
        return "white"
    else:
        return "black"
    
def run(): 
    """
    Main function to run the Othello game.
    
    This function creates the game window, initializes the board, and
    contains the main game loop handling player moves and AI responses.
    """
    # setup
    win = GraphWin("Othello", 1300,875)
    board = Grid(win)
    tiles = board.getTiles()
    controller = Controller(tiles, win)
    quitButton = Button(Point(100,700), 75, 50, "Quit") 
    quitButton.draw(win)
    
    # Add game title above the board
    gameTitle = Text(Point(650, 100), "Game: Othello")
    gameTitle.setSize(24)
    gameTitle.setStyle("bold")
    gameTitle.draw(win)
    
    controller.validMoves()
    # while loop
    discs = 4
    AIColor = "white"
    if AIColor == "white":
        while True: 
            pt = win.getMouse()

            # Process human player's move
            for tile in tiles: 
                if tiles[tile].clicked(pt):
                    controller.turn = oppositeColor(AIColor)
                    controller.getSandwiches(tile)
                    
                    controller.flip2(tile) 
                    
                    controller.changeTurn()
                    new = Piece(oppositeColor(AIColor), tiles[tile].getCenter(), win, tile)
                    controller.pieces.append(new)
                    tiles[tile].occupy(oppositeColor(AIColor))
            
            controller.unmarkall()
            scores_moves = {}
            movesNew = getMoves(controller.getPieces(), AIColor)
            
            for move in movesNew:
                movex = move[0]
                movey = move[1]
                
                movepos = movey * 8 + movex
                print(movex, movey)
                w = weighted_score(movex, movey, controller.getPieces(), discs, AIColor, win) 
                scores_moves[movepos] = w
                
            max_score = max(scores_moves.values())
            AI_move = [move for move, score in scores_moves.items() if score == max_score][0]
            
            new = Piece(AIColor, tiles[AI_move].getCenter(), win, AI_move)
            controller.pieces.append(new)              
            new.draw()
            
            controller.getSandwiches(AI_move)
            controller.changeTurn()
            tiles[AI_move].occupy(AIColor)
            
            AImovex, AImovey = convert(AI_move)
            gridx = AImovex * 75 + 400
            gridy = AImovey * 75 + 175
            print(scores_moves)
            print(AImovex, AImovey, max_score)
            
            movesBlack = getMoves(controller.getPieces(), oppositeColor(AIColor))
            for move in movesBlack:
                movex = move[0]
                movey = move[1]
                
                movepos = movey * 8 + movex
                tiles[movepos].mark()
            
            if quitButton.clicked(pt): break

            discs += 1
    else:
        while True: 
            # AI's turn first (black plays first in Othello)
            controller.turn = AIColor
            scores_moves = {}
            movesNew = getMoves(controller.getPieces(), AIColor)
            
            for move in movesNew:
                movex = move[0]
                movey = move[1]
                
                movepos = movey * 8 + movex
                print(movex, movey)
                w = weighted_score(movex, movey, controller.getPieces(), discs, AIColor, win) 
                scores_moves[movepos] = w
                
            max_score = max(scores_moves.values())
            AI_move = [move for move, score in scores_moves.items() if score == max_score][0]
            
            new = Piece(AIColor, tiles[AI_move].getCenter(), win, AI_move)
            controller.pieces.append(new)              
            new.draw()
            
            controller.getSandwiches(AI_move)
            tiles[AI_move].occupy(AIColor)
            
            AImovex, AImovey = convert(AI_move)
            gridx = AImovex * 75 + 400
            gridy = AImovey * 75 + 175
            print(scores_moves)
            print(AImovex, AImovey, max_score)
            controller.changeTurn()
            
            movesBlack = getMoves(controller.getPieces(), oppositeColor(AIColor))
            for move in movesBlack:
                movex = move[0]
                movey = move[1]
                
                movepos = movey * 8 + movex
                tiles[movepos].mark()
  
            # Human player's turn
            pt = win.getMouse()

            for tile in tiles: 
                if tiles[tile].clicked(pt):
                    controller.turn = oppositeColor(AIColor)
                    controller.getSandwiches(tile)
                    
                    controller.flip2(tile) 
                    
                    new = Piece(oppositeColor(AIColor), tiles[tile].getCenter(), win, tile)
                    controller.pieces.append(new)
                    tiles[tile].occupy(oppositeColor(AIColor))
            
            controller.unmarkall()
            
            if quitButton.clicked(pt): break

            discs += 1

if __name__ == "__main__":
    run()
