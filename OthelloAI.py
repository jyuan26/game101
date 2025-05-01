import math
from piece import Piece
        
def avg_distance(x, y, board, color):
    """
    Calculate the average distance between a position (x,y) and all pieces of a specified color.
    
    Args:
        x, y: Coordinates of the position to calculate distance from
        board: List of all pieces on the board
        color: The color of pieces to measure distance to
        
    Returns:
        Average euclidean distance to all pieces of the specified color
    """
    count = 0 
    total_dist = 0
    for piece in board:
        if piece.getColor() == color:
            distance = math.sqrt((piece.getX() - x)**2 + (piece.getY() - y)**2)
            total_dist += distance
            count += 1
        else:
            pass

    average = total_dist / count
    return average

def avg_dist_from_center(board, color):
    """
    Calculate the average distance of all pieces of a color from their center of mass.
    
    Args:
        board: List of all pieces on the board
        color: Color of pieces to calculate the average distance for
        
    Returns:
        Average distance of pieces from their collective center
    """
    center_x, center_y = getCenter(board, color)
    avg_dist = avg_distance(center_x, center_y, board, color)
    return avg_dist

def board_pos(board, x, y):
    """
    Get the piece at a specific board position.
    
    Args:
        board: List of all pieces on the board
        x, y: Coordinates to check
        
    Returns:
        The piece object at position (x,y) or 0 if the space is empty
    """
    for piece in board:
        if piece.getX() == x and piece.getY() == y:
            return piece
    return 0  # Empty space

def getMoves(board, color):
    """
    Get all valid moves for a specified color.
    
    Args:
        board: List of all pieces on the board
        color: Color for which to find valid moves
        
    Returns:
        List of (x,y) tuples representing valid move positions
    """
    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    opponent_color = 'white' if color == 'black' else 'black'
    valid_moves = set()

    for piece in board:
        if piece.getColor() != color:
            continue
        start_x = piece.getX()
        start_y = piece.getY()

        for dx, dy in directions:
            x, y = start_x + dx, start_y + dy
            has_opponent_piece = False

            while 0 <= x < 8 and 0 <= y < 8:
                tile = board_pos(board, x, y)
                if tile == 0:
                    if has_opponent_piece:
                        valid_moves.add((x, y))
                    break
                elif tile.getColor() == opponent_color:
                    has_opponent_piece = True
                else:  # Same color piece
                    break

                x += dx
                y += dy

    return list(valid_moves)
                
def move(board, x, y, color, win):
    """
    Simulate making a move at position (x,y) and return the resulting board state.
    
    Args:
        board: Current state of the board
        x, y: Coordinates of the move
        color: Color making the move
        win: Graphics window object
        
    Returns:
        New board state after making the move (without modifying the original)
    """
    gridx = x * 75 + 400
    gridy = y * 75 + 175
    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    opponent_color = 'white' if color == 'black' else 'black'

    # Recreate the board using new Piece instances with existing position and pos
    new_board = [Piece(p.getColor(), (p.getX(), p.getY()), win, p.pos) for p in board]

    # Add the new piece at (x, y) using win and a placeholder pos (could be computed if needed)
    # For simplicity, we'll just assume pos = (x, y) unless pos is strictly needed for rendering
    new_piece = Piece(color, (gridx, gridy), win, 8 * y + x)  # or whatever default works for your pos
    new_board.append(new_piece)

    # Check in all 8 directions for pieces to flip
    for dx, dy in directions:
        cx, cy = x + dx, y + dy
        path = []

        while 0 <= cx < 8 and 0 <= cy < 8:
            curr = board_pos(new_board, cx, cy)
            if curr == 0:
                break
            elif curr.getColor() == opponent_color:
                path.append(curr)
            elif curr.getColor() == color:
                for p in path:
                    p.flipColor()
                break
            else:
                break

            cx += dx
            cy += dy

    return new_board

def weighted_score(x, y, board, discs, color, win):
    """
    Calculate a weighted score for a move at position (x,y).
    
    The weights for different score components (flipping, utility, clumping) 
    vary based on the game phase (early, mid, late).
    
    Args:
        x, y: Coordinates of the potential move
        board: Current state of the board
        discs: Number of discs currently on the board
        color: Color making the move
        win: Graphics window object
        
    Returns:
        Total weighted score for the move
    """
    if discs <= 20:
        #early game favors gaining corners, stable pieces, and positioning.
        #High utility weight, very low flipping weight and low clumping weight
        flipping_weight = 0.05
        utility_weight = 0.7
        clumping_weight = 0.25
    elif discs <= 40:
        #midgame favors building a strong structure that will not have a huge
        #amount of discs flipped during endgame. Medium utility weight (since
        #utility includes stable pieces), high clumping weight, and low
        #flipping weight
        flipping_weight = 0.2
        utility_weight = 0.4
        clumping_weight = 0.4
    else:
        #endgame favors flipping as many discs as possible to win the game.
        #Very high flipping weight, 0 utility weight, and low clumping weight.
        flipping_weight = 0.85
        utility_weight = 0.0
        clumping_weight = 0.15

    flip_score, utility_score, clumping_score = score(board, x, y, color, win)
    total_score = flipping_weight*flip_score + utility_weight*utility_score + clumping_weight*clumping_score
    return total_score
    
def stable(x, y, board, color):
    """
    Determine if a piece at position (x,y) would be stable.
    
    A piece is considered stable if it cannot be flipped in future moves.
    This checks all directions to see if the piece is locked in place.
    
    Args:
        x, y: Coordinates to check for stability
        board: Current state of the board
        color: Color of the piece to check
        
    Returns:
        Boolean indicating if the position is stable
    """
    #checks if square is "stable"
    #in the up/down, 2 diagonals, and left/right directions, if there are
    #empty spaces in both directions or an opponent piece in one direction
    #and an empty space in the other direction, the piece is not stable.
    #If not, it is stable.
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for (dx, dy) in directions:
        found_empty_one_way = False
        found_empty_other_way = False
        found_opponent_one_way = False
        found_opponent_other_way = False

        #Check forwards
        #print(x, y)
        row, col = x + dx, y + dy
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board_pos(board, row, col)
            if piece != 0 and piece.getColor() != color:
                found_opponent_one_way = True
                break
            row += dx
            col += dy
            
        row, col = x + dx, y + dy
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board_pos(board, row, col)
            if piece == 0:
                found_empty_one_way = True
                break
            row += dx
            col += dy
            

        #Check backwards
        row, col = x - dx, y - dy
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board_pos(board, row, col)
            if piece != 0 and piece.getColor() != color:
                found_opponent_one_way = True
                break
            row -= dx
            col -= dy
            
        row, col = x - dx, y - dy
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board_pos(board, row, col)
            if piece == 0:
                found_empty_one_way = True
                break
            row -= dx
            col -= dy

        #If opponent pieces exist on both sides or there are blank square on both sides, the piece is unstable
        if found_empty_one_way:
            if found_empty_other_way or found_opponent_other_way:
                return False
        else:
            if found_opponent_one_way and found_empty_other_way:
                return False
        
    return True

def getCenter(board, color):
    """
    Calculate the center of mass for all pieces of a specific color.
    
    Args:
        board: List of all pieces on the board
        color: Color for which to calculate the center
        
    Returns:
        Tuple (center_x, center_y) representing the center of mass
    """
    xsum = 0
    ysum = 0
    disc_count = 0
    for disc in board:
        if disc.getColor() != color:
            continue
        else:
            xsum += disc.getX()
            ysum += disc.getY()
            disc_count += 1

    center_x = xsum / disc_count
    center_y = ysum / disc_count
    return center_x, center_y

def utility(board, x, y, color):
    """
    Calculate the utility score for a position based on strategic value.
    
    Different positions on the board have different strategic values:
    - Corners are extremely valuable (100 pts)
    - Stable pieces are very valuable (80 pts)
    - Center squares are moderately valuable (20 pts)
    - Squares diagonally adjacent to corners are bad (0 pts)
    - Other positions have medium value (25 pts)
    
    Args:
        board: Current state of the board
        x, y: Position to evaluate
        color: Color making the move
        
    Returns:
        Utility score for the position
    """
    opp_color = 0
    if color == "black":
        opp_color = "white"
    else:
        opp_color = "black"
    score = 0
    #corner
    if x == 0 and y == 0 or x == 0 and y == 7 or x == 7 and y == 0 or x == 7 and y == 7:
        score = 100
    #if stable
    elif stable(x, y, board, color):
        score = 80
    #center
    elif x in [2,3,4,5] and y in [2,3,4,5]:
        score = 20
    #diagonally adjacent to corner (bad)
    elif x in [1, 6] and y in [1,6]:
        score = 0
    #anything else
    else:
        score = 25

    #add bonus if stable
    if stable(x, y, board, color):
        score += 20

    return score

def count_corners(board, color):
    """
    Count the number of corners occupied by pieces of a specific color.
    
    Args:
        board: List of all pieces on the board
        color: Color of pieces to count
        
    Returns:
        Number of corners occupied by the specified color
    """
    corners = 0
    for disc in board:
        if disc.getX() in [0, 7] and disc.getY() in [0, 7] and disc.getColor() == color:
            corners += 1

    return corners

def count_discs(board, color):
    """
    Count the number of discs of a specific color on the board.
    
    Args:
        board: List of all pieces on the board
        color: Color of pieces to count
        
    Returns:
        Number of discs of the specified color
    """
    return sum(1 for disc in board if disc.getColor() == color)

def score(before_board, x, y, color, win):
    """
    Calculate the composite score for a move by simulating the move and potential opponent responses.
    
    This evaluates:
    - Flip score: How many discs remain after the opponent's best counter-move
    - Utility score: Strategic value of the position
    - Distance score: How well the move fits with the current piece formation
    
    Args:
        before_board: Current state of the board
        x, y: Position of the potential move
        color: Color making the move
        win: Graphics window object
        
    Returns:
        Tuple of (flip_score, utility_score, distance_score)
    """
    if color == "white":
        opp_color = "black"
    else:
        opp_color = "white"
    #returns 4 "score" values: flipping, utility, distance, util_diff
    #number of discs the player has before the opponent moves
    discs_before = count_discs(before_board, color)
    after_board = move(before_board, x, y, color, win)
    #loop through all possible moves and take into account the worst possible loss of discs
    worst_diff = 100
    #tracks the worst difference between player corner count and opponent corner count
    #tracks worst difference between player utility score and opponent util score
    worst_utility_diff = 1000
    for possible_move in getMoves(after_board, opp_color):
        #board after opponent does possible_move
        opp_move_board = move(after_board, possible_move[0], possible_move[1], opp_color, win)
        #the number of discs of the player after the opponent moves
        discs_after = count_discs(opp_move_board, color)
        #the amount of discs the opponent flipped
        diff = discs_after - discs_before
        #keep track of the most amount of discs the opponent can flip with the next move
        if diff < worst_diff:
            worst_diff = diff

        #calculate utility score difference between player and opponent after opponent's move
        opp_util = utility(after_board, possible_move[0], possible_move[1], opp_color)
        player_util = utility(opp_move_board, x, y, color)
        utility_diff = player_util - opp_util
        if utility_diff < worst_utility_diff:
            worst_utility_diff = utility_diff


    flip_score = 10*worst_diff
    utility_score = (utility(before_board, x, y, color) + 2 * worst_utility_diff)/3
    distance_score = 100-20*avg_distance(x, y, before_board, color)

    return flip_score, utility_score, distance_score
