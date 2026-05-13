from config import settings
from openai import OpenAI
from prompts import TICTACTOE_PROMPT, CONNECT_FOUR_PROMPT
from models import tictactoe as ttc_schemas
from models import connectfour as cf_schemas

def generate_AI_player(board, player: str, available_moves):

    client = OpenAI(api_key=settings.openai_api_key)

    # determine game based on board shape
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
