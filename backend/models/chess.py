from pydantic import BaseModel, Field
from typing import Optional

class Move(BaseModel):
    """Class to represent a chess move"""
    from_square: str | None
    to_square: str | None
    promotion: str | None

class CommentaryLLM(BaseModel):
    player_move_analysis: str | None = Field(description="LLM performs an analysis on the player move made")
    engine_move_analysis: str | None = Field(description="LLM performs an analysis on the engine move made")
    position_summary: str = Field(description="LLM performs an analysis on the game position")


class GenerateMoveRequest(BaseModel):
    """ class to represent what the backend accepts from the client"""
    fen_before: str
    player_move: Move


class GenerateMoveResponse(BaseModel):
    """ class to represent what the backend sends to the client"""
    fen: str
    #engine_move: Move 
    status: str 
    winner: str | None
    player_move_analysis: str | None
    engine_move_analysis: str | None
    position_summary: str | None


