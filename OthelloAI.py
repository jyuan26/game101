import math
from piece import Piece
import functools

# Cache decorator for functions with hashable arguments
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# Board position cache to avoid linear search
def create_board_dict(board):
    board_dict = {}
    for piece in board:
        board_dict[(piece.getX(), piece.getY())] = piece
    return board_dict
        
def avg_distance(x, y, board, color):
    count = 0 
    total_dist = 0
    for piece in board:
        if piece.getColor() == color:
            distance = math.sqrt((piece.getX() - x)**2 + (piece.getY() - y)**2)
            total_dist += distance
            count += 1
    
    if count == 0:  # Handle edge case of no pieces
        return 0
    average = total_dist / count
    return average

def avg_dist_from_center(board, color):
    center_x, center_y = getCenter(board, color)
    avg_dist = avg_distance(center_x, center_y, board, color)
    return avg_dist

def board_pos(board, x, y, board_dict=None):
    # Use dictionary lookup if provided (O(1) instead of O(n))
    if board_dict is not None:
        return board_dict.get((x, y), 0)
    
    # Fall back to original implementation
    for piece in board:
        if piece.getX() == x and piece.getY() == y:
            return piece
    return 0  # Empty space

def getMoves(board, color, board_dict=None):
    if board_dict is None:
        board_dict = create_board_dict(board)
        
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
                tile = board_pos(board, x, y, board_dict)
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
                
def move(board, x, y, color, win, board_dict=None):
    if board_dict is None:
        board_dict = create_board_dict(board)
        
    gridx = x * 75 + 400
    gridy = y * 75 + 175
    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    opponent_color = 'white' if color == 'black' else 'black'

    # Recreate the board using new Piece instances with existing position and pos
    new_board = [Piece(p.getColor(), (p.getX(), p.getY()), win, p.pos) for p in board]
    
    # Create a new board dictionary for the new board
    new_board_dict = create_board_dict(new_board)

    # Add the new piece at (x, y) using win and a placeholder pos
    new_piece = Piece(color, (gridx, gridy), win, 8 * y + x)
    new_board.append(new_piece)
    new_board_dict[(x, y)] = new_piece

    for dx, dy in directions:
        cx, cy = x + dx, y + dy
        path = []

        while 0 <= cx < 8 and 0 <= cy < 8:
            curr = board_pos(new_board, cx, cy, new_board_dict)
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

    return new_board, new_board_dict

def weighted_score(x, y, board, discs, color, win):
    # Set weights based on game phase
    if discs <= 20:
        # Early game favors gaining corners, stable pieces, and positioning.
        # High utility weight, very low flipping weight and low clumping weight
        flipping_weight = 0.05
        utility_weight = 0.7
        clumping_weight = 0.25
    elif discs <= 40:
        # Midgame favors building a strong structure
        flipping_weight = 0.2
        utility_weight = 0.4
        clumping_weight = 0.4
    else:
        # Endgame favors flipping as many discs as possible to win the game.
        flipping_weight = 0.85
        utility_weight = 0.0
        clumping_weight = 0.15

    # Create board dictionary once to use throughout the calculation
    board_dict = create_board_dict(board)
    
    # Get scores with optimized lookup
    flip_score, utility_score, clumping_score = score(board, x, y, color, win, board_dict, discs)
    
    # Calculate weighted score
    total_score = flipping_weight*flip_score + utility_weight*utility_score + clumping_weight*clumping_score
    return total_score
    
def stable(x, y, board, color, board_dict=None):
    if board_dict is None:
        board_dict = create_board_dict(board)
        
    # Check for corners (always stable)
    if (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
        return True
        
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for (dx, dy) in directions:
        found_empty_one_way = False
        found_opponent_one_way = False
        
        # Check forwards in one pass
        row, col = x + dx, y + dy
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board_pos(board, row, col, board_dict)
            if piece == 0:
                found_empty_one_way = True
                break
            if piece.getColor() != color:
                found_opponent_one_way = True
                break
            row += dx
            col += dy
        
        # Check backwards in one pass
        found_empty_other_way = False
        found_opponent_other_way = False
        row, col = x - dx, y - dy
        while 0 <= row < 8 and 0 <= col < 8:
            piece = board_pos(board, row, col, board_dict)
            if piece == 0:
                found_empty_other_way = True
                break
            if piece.getColor() != color:
                found_opponent_other_way = True
                break
            row -= dx
            col -= dy

        # Determine stability based on found pieces
        if found_empty_one_way and (found_empty_other_way or found_opponent_other_way):
            return False
        if found_empty_other_way and (found_empty_one_way or found_opponent_one_way):
            return False
        if found_opponent_one_way and found_empty_other_way:
            return False
        
    return True

def getCenter(board, color):
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

    if disc_count == 0:  # Handle edge case
        return 3.5, 3.5  # Center of the board
        
    center_x = xsum / disc_count
    center_y = ysum / disc_count
    return center_x, center_y

# Memoize utility function for frequently calculated positions
@memoize
def utility_cached(x, y, color, board_string):
    """Cached version of utility that uses a string representation of the board"""
    # We don't actually use board_string in the function, it's just for the cache key
    # The real board is accessed through the closure
    # This is a trick to make the board hashable for caching
    
    score = 0
    # Corner positions (highest value)
    if x == 0 and y == 0 or x == 0 and y == 7 or x == 7 and y == 0 or x == 7 and y == 7:
        return 100
    # Center positions (medium value)
    elif x in [2,3,4,5] and y in [2,3,4,5]:
        score = 20
    # Diagonally adjacent to corner (bad)
    elif x in [1, 6] and y in [1,6]:
        score = 0
    # Everything else
    else:
        score = 25
        
    return score

def utility(board, x, y, color, board_dict=None, check_stable=True):
    if board_dict is None:
        board_dict = create_board_dict(board)
        
    # Get opponent color
    opp_color = "white" if color == "black" else "black"
    
    # Get base utility without stability check
    # Corner positions (highest value)
    if x == 0 and y == 0 or x == 0 and y == 7 or x == 7 and y == 0 or x == 7 and y == 7:
        score = 100
    # Center positions (medium value)
    elif x in [2,3,4,5] and y in [2,3,4,5]:
        score = 20
    # Diagonally adjacent to corner (bad)
    elif x in [1, 6] and y in [1,6]:
        score = 0
    # Everything else
    else:
        score = 25
    
    # Only check stability if requested (it's expensive)
    if check_stable:
        # Check stability once and reuse result
        is_stable = stable(x, y, board, color, board_dict)
        if is_stable:
            if score < 80:  # Only override if better than current score
                score = 80
            score += 20  # Add stability bonus
    
    return score

def count_corners(board, color):
    corners = 0
    for disc in board:
        if disc.getX() in [0, 7] and disc.getY() in [0, 7] and disc.getColor() == color:
            corners += 1
    return corners

def count_discs(board, color):
    return sum(1 for disc in board if disc.getColor() == color)

def score(before_board, x, y, color, win, board_dict=None, discs=None):
    if board_dict is None:
        board_dict = create_board_dict(before_board)
        
    if color == "white":
        opp_color = "black"
    else:
        opp_color = "white"
        
    # Returns 3 score values: flipping, utility, distance
    # Get current disc count
    discs_before = count_discs(before_board, color)
    
    # Make move and get updated board with its dictionary
    after_board, after_board_dict = move(before_board, x, y, color, win, board_dict)
    
    # Limit opponent move simulation in endgame to improve performance
    limited_lookahead = discs is not None and discs > 50
    
    # Initialize worst scores
    worst_diff = 100
    worst_utility_diff = 1000
    
    # Get possible opponent moves
    opp_moves = getMoves(after_board, opp_color, after_board_dict)
    
    # Limit number of opponent moves to consider in endgame
    if limited_lookahead and len(opp_moves) > 3:
        # Prioritize corner moves and sort by position
        corner_moves = [m for m in opp_moves if m[0] in [0, 7] and m[1] in [0, 7]]
        if corner_moves:
            opp_moves = corner_moves
        else:
            # Take first 3 moves only
            opp_moves = opp_moves[:3]
    
    # Calculate worst outcomes from opponent's possible moves
    for possible_move in opp_moves:
        # Board after opponent's move
        opp_move_board, opp_move_board_dict = move(after_board, possible_move[0], possible_move[1], opp_color, win, after_board_dict)
        
        # The number of discs of the player after the opponent moves
        discs_after = count_discs(opp_move_board, color)
        
        # The amount of discs the opponent flipped
        diff = discs_after - discs_before
        
        # Keep track of the most amount of discs the opponent can flip
        if diff < worst_diff:
            worst_diff = diff

        # Calculate utility scores with optimized lookup
        # Skip stability check for faster calculation
        opp_util = utility(after_board, possible_move[0], possible_move[1], opp_color, after_board_dict, check_stable=False)
        player_util = utility(opp_move_board, x, y, color, opp_move_board_dict, check_stable=False)
        
        utility_diff = player_util - opp_util
        if utility_diff < worst_utility_diff:
            worst_utility_diff = utility_diff

    # Calculate final scores
    flip_score = 10 * worst_diff
    utility_score = (utility(before_board, x, y, color, board_dict) + 2 * worst_utility_diff) / 3
    
    # Optimize distance calculation for endgame
    if limited_lookahead:
        distance_score = 50  # Use average value to avoid calculation
    else:
        distance_score = 100 - 20 * avg_distance(x, y, before_board, color)

    return flip_score, utility_score, distance_score
