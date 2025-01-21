import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import List, Tuple, Optional


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        # Game state
        self.current_player = "X"
        self.board = []
        self.game_mode = "2 Players"  # Default mode
        self.ai_difficulty = "Easy"  # Default difficulty
        self.ai_symbol = "O"  # AI always plays as O

        # Create game mode selection
        self.create_game_controls()

        # Create the game board
        self.create_game_board()

        # Reset button
        reset_button = tk.Button(
            self.window,
            text="Reset Game",
            font=('Arial', 12),
            command=self.reset_game
        )
        reset_button.grid(row=5, column=0, columnspan=3, pady=10)

    def create_game_controls(self):
        # Game mode frame
        control_frame = ttk.LabelFrame(self.window, text="Game Settings", padding=10)
        control_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        # Mode selection
        ttk.Label(control_frame, text="Game Mode:").grid(row=0, column=0, padx=5)
        self.mode_var = tk.StringVar(value="2 Players")
        mode_cb = ttk.Combobox(control_frame, textvariable=self.mode_var)
        mode_cb['values'] = ('2 Players', 'vs Computer')
        mode_cb['state'] = 'readonly'
        mode_cb.grid(row=0, column=1, padx=5)
        mode_cb.bind('<<ComboboxSelected>>', self.on_mode_change)

        # Difficulty selection
        ttk.Label(control_frame, text="AI Difficulty:").grid(row=0, column=2, padx=5)
        self.diff_var = tk.StringVar(value="Easy")
        diff_cb = ttk.Combobox(control_frame, textvariable=self.diff_var)
        diff_cb['values'] = ('Easy', 'Medium', 'Hard')
        diff_cb['state'] = 'readonly'
        diff_cb.grid(row=0, column=3, padx=5)

    def create_game_board(self):
        # Create game board frame
        board_frame = ttk.Frame(self.window, padding=10)
        board_frame.grid(row=1, column=0, columnspan=3)

        # Create buttons for the game board
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=('Arial', 20),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.board.append(row)

    def on_mode_change(self, event):
        self.game_mode = self.mode_var.get()
        self.reset_game()

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j]["text"] == "":
                    empty_cells.append((i, j))
        return empty_cells

    def make_ai_move(self):
        difficulty = self.diff_var.get()

        if difficulty == "Easy":
            self.make_random_move()
        elif difficulty == "Medium":
            self.make_medium_move()
        else:  # Hard
            self.make_minimax_move()

    def make_random_move(self):
        empty_cells = self.get_empty_cells()
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def make_medium_move(self):
        # First check if AI can win
        winning_move = self.find_winning_move(self.ai_symbol)
        if winning_move:
            self.make_move(*winning_move)
            return

        # Then check if player can win and block
        blocking_move = self.find_winning_move("X")
        if blocking_move:
            self.make_move(*blocking_move)
            return

        # Otherwise make a random move
        self.make_random_move()

    def find_winning_move(self, symbol: str) -> Optional[Tuple[int, int]]:
        empty_cells = self.get_empty_cells()

        for row, col in empty_cells:
            # Try the move
            self.board[row][col]["text"] = symbol

            # Check if it's a winning move
            if self.check_winner(symbol):
                # Undo the move
                self.board[row][col]["text"] = ""
                return (row, col)

            # Undo the move
            self.board[row][col]["text"] = ""

        return None

    def make_minimax_move(self):
        best_score = float('-inf')
        best_move = None

        for row, col in self.get_empty_cells():
            self.board[row][col]["text"] = self.ai_symbol
            score = self.minimax(False)
            self.board[row][col]["text"] = ""

            if score > best_score:
                best_score = score
                best_move = (row, col)

        if best_move:
            self.make_move(*best_move)

    def minimax(self, is_maximizing: bool) -> int:
        if self.check_winner(self.ai_symbol):
            return 1
        elif self.check_winner("X"):
            return -1
        elif self.check_draw():
            return 0

        empty_cells = self.get_empty_cells()

        if is_maximizing:
            best_score = float('-inf')
            symbol = self.ai_symbol
        else:
            best_score = float('inf')
            symbol = "X"

        for row, col in empty_cells:
            self.board[row][col]["text"] = symbol
            score = self.minimax(not is_maximizing)
            self.board[row][col]["text"] = ""

            if is_maximizing:
                best_score = max(score, best_score)
            else:
                best_score = min(score, best_score)

        return best_score

    def make_move(self, row: int, col: int):
        self.board[row][col]["text"] = self.current_player

        if self.check_winner(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
        elif self.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"

            # If it's AI's turn, make the move
            if self.game_mode == "vs Computer" and self.current_player == self.ai_symbol:
                self.window.after(500, self.make_ai_move)  # Small delay for better UX

    def button_click(self, row: int, col: int):
        # Only allow moves if it's the player's turn
        if (self.game_mode == "vs Computer" and
                self.current_player == self.ai_symbol):
            return

        # Check if the button is empty
        if self.board[row][col]["text"] == "":
            self.make_move(row, col)

    def check_winner(self, player: str) -> bool:
        # Check rows
        for i in range(3):
            if (self.board[i][0]["text"] == self.board[i][1]["text"] ==
                    self.board[i][2]["text"] == player):
                return True

        # Check columns
        for i in range(3):
            if (self.board[0][i]["text"] == self.board[1][i]["text"] ==
                    self.board[2][i]["text"] == player):
                return True

        # Check diagonals
        if (self.board[0][0]["text"] == self.board[1][1]["text"] ==
                self.board[2][2]["text"] == player):
            return True

        if (self.board[0][2]["text"] == self.board[1][1]["text"] ==
                self.board[2][0]["text"] == player):
            return True

        return False

    def check_draw(self) -> bool:
        return all(self.board[i][j]["text"] != ""
                   for i in range(3)
                   for j in range(3))

    def reset_game(self):
        # Clear all buttons and reset current player
        for i in range(3):
            for j in range(3):
                self.board[i][j]["text"] = ""
        self.current_player = "X"

        # If playing against AI and AI goes first, make its move
        if (self.game_mode == "vs Computer" and
                self.current_player == self.ai_symbol):
            self.window.after(500, self.make_ai_move)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()