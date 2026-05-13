from models import chess as chess_schemas
from llm_service import chess_lmm
import chess
from chess_engine.stockfish_engine import sf, get_stockfish_move
from fastapi import APIRouter

router = APIRouter()

@router.post("", response_model = chess_schemas.GenerateMoveResponse)
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

        commentary = chess_lmm.generate_chess_commentary(
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
        commentary = chess_lmm.generate_chess_commentary(
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

    commentary = chess_lmm.generate_chess_commentary(
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