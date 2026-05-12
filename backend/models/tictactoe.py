from pydantic import BaseModel, Field
from typing import Optional

class Move(BaseModel):
    """Class to represent a Tic Tac Toe move"""
    row: int | None = Field(ge=0, le=2, description="The row of the move")
    col: int | None = Field(ge=0, le=2, description="The column of the move")

class GenerateMoveRequestLLM(BaseModel):
    """ class to represent what the backend accepts from the client"""
    board: list[list[Optional[str]]]
    ai_player: str
    human_player: str

class GenerateMoveResponseLLM(BaseModel):
    """ class to represent what the backend sends to the client"""
    winner: str | None
    board: list[list[Optional[str]]]