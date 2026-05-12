from fastapi import FastAPI
from models import connectfour as cf_schemas
from models import tictactoe as ttc_schemas
from models import chess as chess_schemas
from games import TicTacToe, ConnectFour
from llm_service import generate_AI_player, generate_chess_commentary
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import numpy as np
import random
from pathlib import Path
from stockfish import Stockfish
import chess
import os

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", settings.local_stockfish_path)

sf = Stockfish(path=STOCKFISH_PATH)


def get_stockfish_move(board: chess.Board):
    """
    Ask Stockfish for the best move in the current position.
    Returns a python-chess Move object.
    """

    # Give Stockfish the current position
    sf.set_fen_position(board.fen())

    # Ask Stockfish for the best move in UCI format, e.g. "e7e5"
    best_move_uci = sf.get_best_move()

    if best_move_uci is None:
        raise ValueError("Stockfish could not find a move.")

    # Convert "e7e5" into a python-chess Move object
    engine_move = chess.Move.from_uci(best_move_uci)

    # make sure Stockfish's move is legal
    if engine_move not in board.legal_moves:
        raise ValueError(f"Stockfish returned an illegal move: {best_move_uci}")

    return engine_move


app = FastAPI()

# allow origins, methods, and request headers from approved origins to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/tictactoe-move", response_model= ttc_schemas.GenerateMoveResponseLLM)
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
    row, column = generate_AI_player(game.board, ai_player, available_moves)

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
    


@app.post("/api/connectfour-move", response_model= cf_schemas.GenerateMoveResponseLLM)
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
    row, column = generate_AI_player(game.board, ai_player, available_moves)
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



@app.post("/api/chess-move", response_model = chess_schemas.GenerateMoveResponse)
def generate_chess_move(request: chess_schemas.GenerateMoveRequest):
    board = chess.Board(request.fen_before)

    player_move = request.player_move.from_square + request.player_move.to_square + (request.player_move.promotion or "")

    player_move = chess.Move.from_uci(player_move)

    # Make the move
    board.push(player_move)

    # Get new board after player move
    fen_after_user_move = board.fen()

     # Check if the user won
    if board.is_checkmate():

        status = "checkmate"

        commentary = generate_chess_commentary(
            fen_before=request.fen_before,
            player_move=request.player_move,
            fen_after_user_move=fen_after_user_move,
            engine_move=None,
            fen_after_engine_move=board.fen(),
            status=status,
        )

        return {
            "fen": board.fen(),
            "status": status,
            "winner": "player",
            "player_move_analysis": commentary.player_move_analysis,
            "engine_move_analysis": commentary.engine_move_analysis,
            "position_summary": commentary.position_summary,
        }

    if board.is_stalemate() or board.is_insufficient_material():
        status = "draw"
        commentary = generate_chess_commentary(
            fen_before=request.fen_before,
            player_move=request.player_move,
            fen_after_user_move=fen_after_user_move,
            engine_move=None,
            fen_after_engine_move=board.fen(),
            status=status,
        )

        return {
            "fen": board.fen(),
            "status": status,
            "winner": None,
            "player_move_analysis": commentary.player_move_analysis,
            "engine_move_analysis": commentary.engine_move_analysis,
            "position_summary": commentary.position_summary,
        }
    
    # If game continues, ask engine for a move
    engine_move = get_stockfish_move(board)

    # Let engine make move
    board.push(engine_move)

    fen_after_engine_move = board.fen()

    if board.is_checkmate():
        status = "checkmate"
        winner = "engine"
    elif board.is_stalemate() or board.is_insufficient_material():
        status = "draw"
        winner = None
    else:
        status = "ongoing"
        winner = None

    engine_move_schema = chess_schemas.Move(
        from_square=chess.square_name(engine_move.from_square),
        to_square=chess.square_name(engine_move.to_square),
        promotion=chess.piece_symbol(engine_move.promotion) if engine_move.promotion else None,
    )

    commentary = generate_chess_commentary(
        fen_before=request.fen_before,
        player_move=request.player_move,
        fen_after_user_move=fen_after_user_move,
        engine_move=engine_move_schema,
        fen_after_engine_move=fen_after_engine_move,
        status=status,
    )

    return {
        "fen": fen_after_engine_move,
        "status": status,
        "winner": winner,
        "player_move_analysis": commentary.player_move_analysis,
        "engine_move_analysis": commentary.engine_move_analysis,
        "position_summary": commentary.position_summary,
    }

    






    


