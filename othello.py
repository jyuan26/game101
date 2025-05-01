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
    
    # Add AI status below the title
    AIColor = "white"  # We'll define AIColor earlier for use in this text
    AIText = Text(Point(650, 130), f"AI is playing: {AIColor.capitalize()}")
    AIText.setSize(18)
    AIText.draw(win)
    
    # Add current move indicator below the board
    moveText = Text(Point(650, 800), "Current Move: Black")
    moveText.setSize(18)
    moveText.draw(win)
    
    # Add AI calculation status text
    statusText = Text(Point(650, 830), "")
    statusText.setSize(14)
    statusText.draw(win)
    
    # Add mouse click position display
    clickPosText = Text(Point(650, 860), "")
    clickPosText.setSize(14)
    clickPosText.draw(win)
    
    controller.validMoves()
    # Set initial turn to black (since black plays first in Othello)
    controller.turn = "black"
    # while loop
    discs = 4
    if AIColor == "white":
        while True: 
            pt = win.getMouse()
            
            # Display mouse click position
            clickX, clickY = pt.getX(), pt.getY()
            clickPosText.setText(f"Mouse Clicked Position: {int(clickX)}, {int(clickY)}")
            
            # Check for quit button press immediately
            if quitButton.clicked(pt): 
                win.close()
                return

            # Process human player's move
            for tile in tiles: 
                if tiles[tile].clicked(pt):
                    controller.turn = oppositeColor(AIColor)
                    controller.getSandwiches(tile)
                    
                    controller.flip2(tile) 
                    
                    controller.changeTurn()
                    new = Piece(oppositeColor(AIColor), tiles[tile].getCenter(), win, tile)
                    new.draw()
                    controller.pieces.append(new)
                    tiles[tile].occupy(oppositeColor(AIColor))
                    
                    # Update move text after human's move
                    moveText.setText(f"Current Move: {controller.turn.capitalize()}")

            
            controller.unmarkall()
                                
            # Display move complete message and wait for click to continue
            statusText.setText("Move complete. Click anywhere to continue to AI move.")
            win.getMouse()
            statusText.setText("")
            
            scores_moves = {}
            movesNew = getMoves(controller.getPieces(), AIColor)
            
            # Show total calculations to be done
            total_calcs = len(movesNew)
            statusText.setText(f"Status: Total: {total_calcs}, Current: 0")
            win.update()
            
            # Check for quit button click before calculations
            click = win.checkMouse()
            if click is not None and quitButton.clicked(click):
                win.close()
                return
                
            for i, move in enumerate(movesNew):
                movex = move[0]
                movey = move[1]
                
                movepos = movey * 8 + movex
                print(movex, movey)
                
                # Update calculation status
                statusText.setText(f"Status: Total: {total_calcs}, Current: {i+1}")
                win.update()
                
                # Check for quit button click during calculations
                click = win.checkMouse()
                if click is not None and quitButton.clicked(click):
                    win.close()
                    return
                
                w = weighted_score(movex, movey, controller.getPieces(), discs, AIColor, win) 
                scores_moves[movepos] = w
            
            # Another check after calculations complete
            click = win.checkMouse()
            if click is not None and quitButton.clicked(click):
                win.close()
                return
                
            # Clear status text after calculations
            statusText.setText("")
            
            max_score = max(scores_moves.values())
            AI_move = [move for move, score in scores_moves.items() if score == max_score][0]
            
            new = Piece(AIColor, tiles[AI_move].getCenter(), win, AI_move)
            controller.pieces.append(new)              
            new.draw()
            
            controller.getSandwiches(AI_move)
            controller.changeTurn()
            tiles[AI_move].occupy(AIColor)
            
            # Update move text after AI's move
            moveText.setText(f"Current Move: {controller.turn.capitalize()}")
            
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
            
            if quitButton.clicked(pt): 
                win.close()
                return

            discs += 1
    else:
        while True: 
            # AI's turn first (black plays first in Othello)
            controller.turn = AIColor
            scores_moves = {}
            movesNew = getMoves(controller.getPieces(), AIColor)
            
            # Show total calculations to be done
            total_calcs = len(movesNew)
            statusText.setText(f"Status: Total: {total_calcs}, Current: 0")
            win.update()
            
            # Check for quit button click before calculations
            click = win.checkMouse()
            if click is not None and quitButton.clicked(click):
                win.close()
                return
                
            for i, move in enumerate(movesNew):
                movex = move[0]
                movey = move[1]
                
                movepos = movey * 8 + movex
                print(movex, movey)
                
                # Update calculation status
                statusText.setText(f"Status: Total: {total_calcs}, Current: {i+1}")
                win.update()
                
                # Check for quit button click during calculations
                click = win.checkMouse()
                if click is not None and quitButton.clicked(click):
                    win.close()
                    return
                
                w = weighted_score(movex, movey, controller.getPieces(), discs, AIColor, win) 
                scores_moves[movepos] = w
            
            # Another check after calculations are complete
            click = win.checkMouse()
            if click is not None and quitButton.clicked(click):
                win.close()
                return
                
            # Clear status text after calculations
            statusText.setText("")
            
            max_score = max(scores_moves.values())
            AI_move = [move for move, score in scores_moves.items() if score == max_score][0]
            
            new = Piece(AIColor, tiles[AI_move].getCenter(), win, AI_move)
            controller.pieces.append(new)              
            new.draw()
            
            controller.getSandwiches(AI_move)
            tiles[AI_move].occupy(AIColor)
            
            # Update move text after AI's move
            moveText.setText(f"Current Move: {controller.turn.capitalize()}")
            
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
            
            # Display mouse click position
            clickX, clickY = pt.getX(), pt.getY()
            clickPosText.setText(f"Mouse Clicked Position: {int(clickX)}, {int(clickY)}")
            
            # Check for quit button press immediately
            if quitButton.clicked(pt): 
                win.close()
                return

            for tile in tiles: 
                if tiles[tile].clicked(pt):
                    controller.turn = oppositeColor(AIColor)
                    controller.getSandwiches(tile)
                    
                    controller.flip2(tile) 
                    
                    new = Piece(oppositeColor(AIColor), tiles[tile].getCenter(), win, tile)
                    controller.pieces.append(new)
                    tiles[tile].occupy(oppositeColor(AIColor))
                    
                    # Update move text after human's move
                    moveText.setText(f"Current Move: {controller.turn.capitalize()}")
                    
                    # Display move complete message and wait for click to continue
                    statusText.setText("Move complete. Click anywhere to continue to AI move.")
                    win.getMouse()
                    statusText.setText("")
            
            controller.unmarkall()
            
            if quitButton.clicked(pt): 
                win.close()
                return

            discs += 1

if __name__ == "__main__":
    run()
