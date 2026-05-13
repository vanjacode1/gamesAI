from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chess, connectfour, tictactoe


app = FastAPI()

# allow origins, methods, and request headers from approved origins to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000","http://localhost:5173","https://gamesai-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tictactoe.router, prefix = "/api/tictactoe-move")
app.include_router(connectfour.router, prefix = "/api/connectfour-move")
app.include_router(chess.router, prefix = "/api/chess-move")