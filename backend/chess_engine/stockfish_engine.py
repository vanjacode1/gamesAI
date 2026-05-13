from pathlib import Path
from stockfish import Stockfish
import chess
import os
from config import settings


STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", settings.stockfish_path)

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