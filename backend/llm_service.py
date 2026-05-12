from config import settings
from openai import OpenAI
from prompts import TICTACTOE_PROMPT, CONNECT_FOUR_PROMPT, CHESS_ANALYSIS_PROMPT
from models import tictactoe as ttc_schemas
from models import connectfour as cf_schemas
from models import chess as chess_schemas

def generate_AI_player(board, player: str, available_moves):

    client = OpenAI(api_key=settings.openai_api_key)

    if board.shape == (3,3):
        game_instructions = TICTACTOE_PROMPT
        llm_output = ttc_schemas.Move

    elif board.shape == (6, 7):
        game_instructions = CONNECT_FOUR_PROMPT
        llm_output = cf_schemas.AIMove

    else:
        raise ValueError("This game is unknown")

    response = client.responses.parse(
    model="gpt-5.4",
    instructions = f"{game_instructions}",
        input=f"""Here is the board: {board.tolist()}. You play as {player}. 
        Your available moves are {available_moves}.
          Return a valid move and try to win according to the game rules.""",
        text_format = llm_output
    )

    move = response.output_parsed

    if board.shape == (3, 3):
        return move.row, move.col

    if board.shape == (6, 7):
        return move.row, move.col



def generate_chess_commentary(
    fen_before: str,
    player_move,
    fen_after_user_move: str,
    engine_move,
    fen_after_engine_move: str,
    status: str,
):
    client = OpenAI(api_key=settings.openai_api_key)

    llm_output = chess_schemas.CommentaryLLM

    instructions = CHESS_ANALYSIS_PROMPT

    response = client.responses.parse(

        model="gpt-5.4",
        instructions = f"{instructions}",
        input=f"""
            Position before the user move:
            {fen_before}

            User move:
            from {player_move.from_square} to {player_move.to_square}
            Promotion: {player_move.promotion}

            Position after the user move:
            {fen_after_user_move}

            Engine move:
            from {engine_move.from_square} to {engine_move.to_square}
            Promotion: {engine_move.promotion}

            Final position after the engine move:
            {fen_after_engine_move}

            Game status:
            {status}

            Explain this turn as a friendly chess coach.
            """,
        text_format=llm_output,
        )

    analysis = response.output_parsed

    return analysis
