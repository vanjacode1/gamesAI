from models import tictactoe as ttc_schemas
from games import TicTacToe
import random
from llm_service import tictactoe_lmm
from fastapi import APIRouter
import numpy as np

router = APIRouter()

@router.post("", response_model= ttc_schemas.GenerateMoveResponseLLM)
def generate_ai_turn(request: ttc_schemas.GenerateMoveRequestLLM):
    game = TicTacToe()

    # get variables sent from the frontend (board, players, human_move)
    game.board = np.array(request.board, dtype=object)
    ai_player = request.ai_player

    # first check if winner or draw
    result = game.check_winner()
    
    if result is not None:
        return {
            "winner": result,
            "board": game.board.tolist()
        }

    # if game didnt end, continue by asking a valid move from the LLM
    available_moves = game.available_moves()
    row, column = tictactoe_lmm.generate_AI_player(game.board, ai_player, available_moves)

    # apply move function internally checks whether a move is valid or not
    # if LLM makes an invalid move, fall back by letting AI make a random available move
    try:
        game.apply_move(ai_player, (row, column))
    except ValueError:
        row, column = random.choice(available_moves)
        game.apply_move(ai_player, (row, column))

    # check if the AI move led to it winning the game or drawing
    result = game.check_winner()
    
    return {
        "winner": result,
        "board": game.board.tolist()
        }