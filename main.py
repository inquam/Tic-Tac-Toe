import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        # Current player (X starts)
        self.current_player = "X"

        # Game board (stores button states)
        self.board = []

        # Create buttons for the game board
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    self.window,
                    text="",
                    font=('Arial', 20),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.board.append(row)

        # Reset button
        reset_button = tk.Button(
            self.window,
            text="Reset Game",
            font=('Arial', 12),
            command=self.reset_game
        )
        reset_button.grid(row=3, column=0, columnspan=3, pady=10)

    def button_click(self, row, col):
        # Check if the button is empty
        if self.board[row][col]["text"] == "":
            self.board[row][col]["text"] = self.current_player

            # Check for win
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            # Check for draw
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                # Switch player
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Check rows
        for i in range(3):
            if (self.board[i][0]["text"] == self.board[i][1]["text"] ==
                    self.board[i][2]["text"] == self.current_player):
                return True

        # Check columns
        for i in range(3):
            if (self.board[0][i]["text"] == self.board[1][i]["text"] ==
                    self.board[2][i]["text"] == self.current_player):
                return True

        # Check diagonals
        if (self.board[0][0]["text"] == self.board[1][1]["text"] ==
                self.board[2][2]["text"] == self.current_player):
            return True

        if (self.board[0][2]["text"] == self.board[1][1]["text"] ==
                self.board[2][0]["text"] == self.current_player):
            return True

        return False

    def check_draw(self):
        for row in self.board:
            for button in row:
                if button["text"] == "":
                    return False
        return True

    def reset_game(self):
        # Clear all buttons and reset current player
        for i in range(3):
            for j in range(3):
                self.board[i][j]["text"] = ""
        self.current_player = "X"

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()