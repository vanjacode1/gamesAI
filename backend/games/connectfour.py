class ConnectFour:
    def __init__(self):
        self.board = [[None] * 7 for _ in range(6)]

    def valid_move(self, move):
        if 0 <= move <= 6:
            return True
        return False
    
    def available_moves(self):
        moves = []
        for col in range(7):
            all_empty_rows = []
            for row in range(6):
                if self.board[row][col] is None:
                    all_empty_rows.append(row)

            if all_empty_rows:
                correct_row = max(all_empty_rows)
                moves.append((correct_row, col))
        return moves
    
    def apply_move_AI(self, player, move):

        # AI chooses row and column
        row, col = move

        if self.board[row][col] is None and 0 <= col <= 6:
            self.board[row][col] = player
        else:
            raise ValueError("This move is not permitted")
    
    def find_row(self, move):
        all_rows = []
        for i in range(6):
            if self.board[i][move] is None:
                all_rows.append(i)

            if all_rows:
                correct_row = max(all_rows)
                return correct_row
            else:
                raise ValueError("This column is completely filled")

            
    def apply_move(self, player, move):

        # player only chooses the column
        col = move

        if self.valid_move(col):
            # find correct row placement to place move
            row = self.find_row(col)
            self.board[row][col] = player

        else:
            raise ValueError("This column does not exist")
            

    def check_winner(self):
        for player in ["Y", "R"]:

            # check horizontal four connected
            for row in range(6):
                for col in range(4):
                    if all(self.board[row][col + i] == player for i in range(4)):
                        return player

            # check vertical four connected
            for row in range(3):
                for col in range(7):
                    if all(self.board[row + i][col] == player for i in range(4)):
                        return player

            #check diagonal four connected:
            for row in range(3):
                for col in range(4):
                    if all(self.board[row + i][col+ i] == player for i in range(4)):
                        return player

            #check diagonal four connected:
            for row in range(5, 1, -1):
                for col in range(4):
                    if all(self.board[row - i][col+ i] == player for i in range(4)):
                        return player
                    
        # if no winner and board full return a draw
        if all(
            cell is not None
            for row in self.board
            for cell in row
        ):
            return "draw"