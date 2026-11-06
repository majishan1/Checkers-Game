from copy import deepcopy
import numpy as np
from constants import RED, BLUE


def Minimax(depth, min_max, board, turn, pruning=False, alpha = - np.inf, beta = np.inf):
    # if there is a winner determined or the search length is reached
    if depth == 0 or board.valid_winner(turn) != None:
        return board.check_board(), board
    
    # if its red turn in the tree
    if min_max:
        maxCheck = - np.inf
        best_choice_m = None
        best_choice_j = None
        decisions, jumps = possible_valid_moves(board, RED)
        
        # Finds the maximum possible value achievable if all teams play optimally
        for i in range(len(decisions)):
            decision = decisions[i]
            jump = jumps[i]
            evaluate = Minimax(depth - 1, False, decision, turn, pruning, alpha, beta)
            maxCheck = max(maxCheck, evaluate[0])
            alpha = max(alpha, evaluate[0])
            if maxCheck == evaluate[0]:
                best_choice_m = decision
                best_choice_j = jump
            if alpha >= beta and pruning:
                break
        
        return maxCheck, best_choice_m, best_choice_j
    
    else:
        minCheck = np.inf
        best_choice_m = None
        best_choice_j = None
        decisions, jumps = possible_valid_moves(board, BLUE)
        # Finds minimum achievable value if both teams play optimally
        for i in range(len(decisions)):
            decision = decisions[i]
            jump = jumps[i]
            evaluate = Minimax(depth - 1, True, decision, turn, pruning, alpha, beta)
            minCheck = min(minCheck, evaluate[0])
            beta = min(beta, evaluate[0])
            if minCheck == evaluate[0]:
                best_choice_m = decision
                best_choice_j = jump
            if alpha <= beta and pruning:
                break
        
        return minCheck, best_choice_m, best_choice_j
    

def possible_valid_moves(board, colour):
    moves = []
    moves_jumps = []
    # finds valid moves for all pieces of the current player's turn in the tree
    for piece in board.find_all_pieces(colour):
        if not piece.is_King():
            valid_moves = board.find_valid_moves(piece, piece.row, piece.col, piece.dir, board.find_blank_spaces(), king_check=False)[0]
        else:
            valid_moves = board.king_movement(piece, piece.row, piece.col, board.find_blank_spaces())
        for key, jump in valid_moves.items():
            temporary_board = deepcopy(board)
            temporary_piece = temporary_board.find_piece(piece.row, piece.col)
            new_board, new_board_jumps = simulate_move(temporary_piece, key, temporary_board, jump)
            moves.append(new_board)
            moves_jumps.append(new_board_jumps)
    
    return moves, moves_jumps

# simulates move using a copy of the board, without altering the state of the current board
def simulate_move(piece, move, board, jump = []):
    board.move(piece, move[0], move[1])
    if jump: 
        board.remove(jump)
    return board, jump
