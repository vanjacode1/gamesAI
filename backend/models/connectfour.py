from pydantic import BaseModel, Field
from typing import Optional


class PlayerMove(BaseModel):
    """Class to represent a Connect Four move"""
    col: int | None = Field(ge=0, le=6, description="The column of the move")

class AIMove(BaseModel):
    """Class to represent a Connect Four move from the AI"""
    row: int | None = Field(ge=0, le=5, description="The row of the move")
    col: int | None = Field(ge=0, le=6, description="The column of the move")

class GenerateMoveRequestLLM(BaseModel):
    """ class to represent what the backend accepts from the client"""
    board: list[list[Optional[str]]]
    ai_player: str
    human_player: str
    #human_move: PlayerMove = Field(description="The column of the human player move")

class GenerateMoveResponseLLM(BaseModel):
    """ class to represent what the backend sends to the client"""
    #ai_move: AIMove = Field(description="The row and column of the AI player move")
    winner: str | None
    board: list[list[Optional[str]]]