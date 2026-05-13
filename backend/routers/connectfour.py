from models import connectfour as cf_schemas
from games import ConnectFour
import random
from fastapi import APIRouter
import numpy as np
from llm_service import connectfour_lmm

router = APIRouter()

@router.post("", response_model= cf_schemas.GenerateMoveResponseLLM)
def generate_ai_turn(request: cf_schemas.GenerateMoveRequestLLM):
    game = ConnectFour()

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
    row, column = connectfour_lmm.generate_AI_player(game.board, ai_player, available_moves)
    print(row, column)

    # apply move function internally checks whether a move is valid or not
    # if LLM makes an invalid move, fall back by letting AI make a random available move
    try:
        game.apply_move_AI(ai_player, (row, column))
    except ValueError:
        row, column = random.choice(available_moves)
        game.apply_move_AI(ai_player, (row, column))

    # check if the AI move led to it winning the game or drawing
    result = game.check_winner()
    
    return {
        "winner": result,
        "board": game.board.tolist()
        }