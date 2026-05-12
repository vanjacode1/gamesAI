from llm_service import generate_AI_player
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.array([[None] * 3 for _ in range(3)])

    def valid_move(self, move):
        row, col = move
        if 0 <= row <= 2 and 0 <= col <= 2 and self.board[row][col] is None:
            return True
        return False
    
    def available_moves(self):
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    moves.append((row, col))

        return moves

    def apply_move(self, player, move):
        if not self.valid_move(move):
            raise ValueError("Invalid move")
        
        row, col = move
        self.board[row][col] = player

    def check_winner(self):

        for player in ["X", "O"]:

            # check winner in rows
            for row in range(3):
                if None not in self.board[row] and all(self.board[row][col] == player for col in range(3)):
                    return player

            # check winner in columns
            for col in range(3):  
                if self.board[0][col] is not None and all(self.board[row][col] == player for row in range(3)):
                   return player

            # check winner diagonals
            if self.board[0][0] is not None and all(self.board[row][row] == player for row in range(3)):
                return player

            if self.board[0][2] is not None and all(self.board[row][2 - row] == player for row in range(3)):
                return player

        # if there is no winner and if board is filled, declare a draw
        if all(
            cell is not None
            for row in self.board
            for cell in row):
                return "draw"


if __name__=="__main__":
    game = TicTacToe()
    
    while True:
        print(game.available_moves())
        ai_player_move = generate_AI_player(game.board, "X", game.available_moves)
        print(ai_player_move)
        game.apply_move("X", ai_player_move)
        print(game.board)
    
        if game.check_winner() is not None:
            print(game.check_winner())
            break
        
        human_player_move_row = int(input("ROW" ))
        human_player_move_col = int(input("col" ))
        game.apply_move("O", (human_player_move_row, human_player_move_col))
        print(game.board)
    
        if game.check_winner() is not None:
            print(game.check_winner())
            break
        
        
        