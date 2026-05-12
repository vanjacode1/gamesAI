from stockfish import Stockfish
import chess


sf = Stockfish(path="chess_engine/stockfish-windows-x86-64-avx2.exe")

# set skill level
sf.set_elo_rating(1500)

board = chess.Board()
board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
print(board)

f = chess.Move.from_uci("g1f3")
board.push(f)
print(board.fen())

print(board.outcome())