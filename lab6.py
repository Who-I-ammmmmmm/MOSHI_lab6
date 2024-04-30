import tkinter as tk
from tkinter import messagebox
import random
import math

player1 = 'X'
player2 = 'O'

# Tic-tac-toe game class for point 6
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Initialize empty 3x3 board
        self.current_winner = None  # Initialize current winner variable

    # Method for making a move
    def make_move(self, square, letter):
        if self.board[square] == ' ':  # Check if the square is empty
            self.board[square] = letter  # Make the move
            if self.winner(square, letter):  # Check for a win after the move
                self.current_winner = letter  # Set the current winner
            return True
        return False

    # Method for checking for a win
    def winner(self, square, letter):
        row_ind = square // 3  # Row index
        row = self.board[row_ind * 3:(row_ind + 1) * 3]  # Get the row
        if all([s == letter for s in row]):  # Check if all elements in the row are equal to the move
            return True
        col_ind = square % 3  # Column index
        column = [self.board[col_ind + i * 3] for i in range(3)]  # Get the column
        if all([s == letter for s in column]):  # Check if all elements in the column are equal to the move
            return True
        if square % 2 == 0:  # If the move is in one of the corners
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # Get diagonal 1
            if all([s == letter for s in diagonal1]):  # Check if all elements in diagonal 1 are equal to the move
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # Get diagonal 2
            if all([s == letter for s in diagonal2]):  # Check if all elements in diagonal 2 are equal to the move
                return True
        return False

    # Get a list of empty squares on the board
    def empty_squares(self):
        return ' ' in self.board

    # Get the number of empty squares on the board
    def num_empty_squares(self):
        return self.board.count(' ')

    # Get available moves
    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

# GUI for tic-tac-toe game for point 5
class TicTacToeGUI:
    def __init__(self, master, x_player, o_player, first_player='pc'):
        global player1, player2
        self.master = master
        self.master.title("Tic Tac Toe")  # Window title
        self.board_buttons = []  # List of buttons on the board
        self.create_board_buttons()  # Create buttons on the board
        self.ttt_game = TicTacToe()  # Create game object
        self.x_player = x_player  # Player X
        self.o_player = o_player  # Player O
        self.current_player = 'X'
        self.first_player = first_player
        if first_player == 'pc':
            self.computer_move()  # If the computer makes the first move
        else:
            player2 = 'X'
            player1 = 'O'


    # Create buttons on the board
    def create_board_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text='', font=('Arial', 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)  # Place buttons on the grid
                self.board_buttons.append(button)  # Add button to the list

    # Handle button click
    def on_button_click(self, row, col):
        if self.ttt_game.make_move(row * 3 + col, self.current_player):  # Make a move
            self.update_button(row, col)  # Update button appearance
            if self.ttt_game.current_winner:  # Check for a win
                self.show_winner()  # Show the winner
                return
            if self.ttt_game.num_empty_squares() == 0:  # Check for a tie
                self.show_tie()  # Show tie message
                return
            self.current_player = player2 if self.current_player == player1 else player1  # Switch player
            if isinstance(self.x_player, SmartComputerPlayer) and self.current_player == player1:
                self.computer_move()  # Computer move

    # Update button appearance after a move
    def update_button(self, row, col):
        index = row * 3 + col
        self.board_buttons[index].config(text=self.ttt_game.board[index], state='disabled')

    # Show win message
    def show_winner(self):
        messagebox.showinfo("Game Over", f"{self.ttt_game.current_winner} wins!")  # Show win message
        self.reset_game()  # Reset the game

    # Show tie message
    def show_tie(self):
        messagebox.showinfo("Game Over", "It's a tie!")  # Show tie message
        self.reset_game()  # Reset the game

    # Computer move
    def computer_move(self):
        if self.current_player == player1:
            square = self.x_player.get_move(self.ttt_game)  # Get move from player X
        else:
            square = self.o_player.get_move(self.ttt_game)  # Get move from player O
        self.ttt_game.make_move(square, self.current_player)  # Make the move
        row, col = divmod(square, 3)  # Get move coordinates
        self.update_button(row, col)  # Update button appearance
        if self.ttt_game.current_winner:  # Check for a win
            self.show_winner()  # Show the winner
            return
        if self.ttt_game.num_empty_squares() == 0:  # Check for a tie
            self.show_tie()  # Show tie message
            return
        self.current_player = player2 if self.current_player == player1 else player1  # Switch player
        if self.current_player == player1:
            self.computer_move()  # Computer move

    # Reset the game
    def reset_game(self):
        self.ttt_game = TicTacToe()  # Create a new game object
        self.current_player = 'X'  # Initialize the current player
        for button in self.board_buttons:
            button.config(text='', state='normal')  # Reset button appearance
        if self.first_player == 'pc':
            self.computer_move() 


# Base player class
class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self):
        pass


# Random computer player class
class RandomComputerPlayer(Player):
    def get_move(self, game):
        return random.choice(game.available_moves())  # Randomly choose a move


# Smart computer player class
class SmartComputerPlayer(Player):
    def get_move(self, game):
        if len(game.available_moves()) == 9:  # If the board is empty
            return random.choice(game.available_moves())  # Random move
        else:
            return self.minimax(game, self.letter)['position']  # Minimax algorithm to determine the best move

    # Minimax algorithm for points 2, 3, and 4
    def minimax(self, state, player):
        max_player = self.letter
        other_player = player2 if player == player1 else player1

        # If the current player wins, return a high score
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        # If it's a tie, return 0
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        # Initialize best move
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        # Iterate through all possible moves
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)  # Make the move
            sim_score = self.minimax(state, other_player)  # Recursive call to minimax for the next move

            state.board[possible_move] = ' '  # Undo the move
            state.current_winner = None  # Reset the current winner
            sim_score['position'] = possible_move  # Record the move position

            # Update the best move
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


# Main part of the program
if __name__ == "__main__":
    root = tk.Tk()  # Create a Tkinter window
    first_player = 'player' # pc - computer starts first, player - you start first
    x_player = SmartComputerPlayer('pc')  # Player X - smart computer
    o_player = 'player'  # Player O - human
    app = TicTacToeGUI(root, x_player, o_player, first_player=first_player)  # Create GUI for tic-tac-toe game, where the first move is made by a human
    root.mainloop()  # Start the main Tkinter loop
