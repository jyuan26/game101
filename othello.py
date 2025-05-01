"""
Othello.py 
Benjamin Bouie 
Othello main 
"""

from piece import Piece 
from grid import Cell, Grid, Controller
from graphics import GraphWin, Point
from button import Button 
from OthelloAI import *

def convert(number):
    row = number // 8
    col = number - 8 * row
    return row, col
    
def run(): 
    # setup
    win = GraphWin("Othello", 1300,875)
    board = Grid(win)
    tiles = board.getTiles()
    controller = Controller(tiles, win)
    quitButton = Button(Point(100,700), 75, 50, "Quit") 
    quitButton.draw(win)
    controller.validMoves()
    w = weighted_score(2, 3, controller.getPieces(), 4, "black", win)
    # while loop
    discs = 4
    while True: 
        pt = win.getMouse()
        for tile in tiles: 
            if tiles[tile].clicked(pt):
                controller.turn = "black"
                controller.getSandwiches(tile)
                
                controller.flip2(tile) 
                ## tile2 = 27
                ##controller.flip(tile2)
                ##new = Piece("black", tiles[tile2].getCenter(), win, tile2)
                ##new.draw()
                
                
                controller.changeTurn()
                new = Piece("black", tiles[tile].getCenter(), win, tile)
                controller.pieces.append(new)
                tiles[tile].occupy("black")
                #moves = controller.validMoves()
        
        scores_moves = {}
        movesNew = getMoves(controller.getPieces(), "white")
        
        ##for move in moves[1]:
        for move in movesNew:
            movex = move[0]
            movey = move[1]
            
            move = movey * 8 + movex
            print(movex, movey)
            w = weighted_score(movex, movey, controller.getPieces(), discs, "white", win) 
            scores_moves[move] = w
            
        max_score = max(scores_moves.values())
        AI_move = [move for move, score in scores_moves.items() if score == max_score][0]
        #controller.turn = "white"
        
        ##controller.flip(AI_move)
        new = Piece("white", tiles[AI_move].getCenter(), win, AI_move)
        controller.pieces.append(new)              
        new.draw()
        ##controller.pieces.append(new)
        
        controller.getSandwiches(AI_move)
        controller.changeTurn()
        tiles[AI_move].occupy("white")
        ##new = Piece("white", tiles[tile].getCenter(), win, tile)
        ##controller.pieces.append(new)              
        ##new.draw()
        
        ##max_score = -100000.0
        ##for score in list(scores_moves.keys()):
        ##    if score > max_score:
        ##        max_score = score

        ##AI_move = scores_moves[max_score]
        
        AImovex, AImovey = convert(AI_move)
        gridx = AImovex * 75 + 400
        gridy = AImovey * 75 + 175
        print(scores_moves)
        print(AImovex, AImovey, max_score)
        
        if quitButton.clicked(pt): break

        discs += 1
            

if __name__ == "__main__":
    run()
