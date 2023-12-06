from ai import AI
from gui import GUI
from functions import check_win, draw_symbol
from tkinter import Event as tkEvent
from random import randint
from typing import Callable


class Game:
    def __init__(self) -> None:
        # Create GUI and AI objects
        self.gui = GUI()
        self.ai = AI("O")

        # Initialise variables
        self.x_score = 0
        self.o_score = 0

        self.game_number = 0
        self.turn_number = 0

        self.game_over = False

        self.callback = None
        self.grid = None

        # Bind functions to menu buttons
        self.gui.friend_btn.configure(
            command=lambda: self.start(self.play_friend)
        )

        self.gui.impossible_btn.configure(
            command=lambda: self.start(lambda e: self.play_ai(e, "impossible"))
        )

        self.gui.normal_btn.configure(
            command=lambda: self.start(lambda e: self.play_ai(e, "normal"))
        )

    def start(self, callback: Callable, from_menu: bool = True) -> None:
        if from_menu:
            # Resets variables to initial values
            self.game_number = 0
            self.turn_number = 0

            self.x_score = 0
            self.o_score = 0

            self.gui.x_score_var.set(f"X score:\n{self.x_score}")
            self.gui.o_score_var.set(f"O score:\n{self.o_score}")

            self.gui.turn_var.set("X to play!")

            # Unbinds potentially bound functions
            self.gui.unbind("<r>")
            self.gui.unbind("<R>")

            for grid_block in self.gui.grid_blocks:
                grid_block.unbind("<Button-1>")
                grid_block.delete("all")

        # Initialises variables for the game
        self.callback = callback
        self.grid = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.game_over = False

        # Displays the grid
        self.gui.menu_to_grid()

        # Binds the callback function
        for grid_block in self.gui.grid_blocks:
            grid_block.bind("<Button-1>", self.callback)

        # Checks if playing AI or friend
        if self.callback == self.play_friend:
            return

        # Hide unused label when playing AI
        self.gui.turn_label.place_forget()

        # Plays the first AI move if necessary
        if self.game_number % 2 != 0:
            self.play_move(randint(0, 8), "O")

    def play_friend(self, e: tkEvent) -> None:
        # Gets the grid index
        grid_index = self.gui.grid_blocks.index(e.widget)

        # Validates the move
        if type(self.grid[grid_index]) != int:
            return

        # Gets the player and opponent
        player = self.get_player()
        opponent = "X" if player == "O" else "O"

        self.gui.turn_var.set(f"{opponent} to play!")

        # Plays the move
        self.play_move(grid_index, player)

    def play_ai(self, e: tkEvent, difficulty: str) -> None:
        # Gets the grid index
        grid_index = self.gui.grid_blocks.index(e.widget)

        # Validates the move
        if type(self.grid[grid_index]) != int:
            return

        # Plays the user's move
        self.play_move(grid_index, "X")

        if not self.game_over:
            # Calculates the index of the AI's move depending on the difficulty
            index = self.ai.get_best_move(self.grid) if difficulty == "impossible" \
                else self.ai.get_normal_move(self.grid)

            # Plays the AI move
            self.play_move(index, "O")

    def new_game(self, callback: Callable) -> None:
        # Unbinds the new_game function
        self.gui.unbind("<r>")
        self.gui.unbind("<R>")

        # Updates variables
        self.game_number += 1
        self.turn_number = 0

        self.gui.turn_var.set(f"{self.get_player()} to play!")

        # Clears the grid GUI
        for grid_block in self.gui.grid_blocks:
            grid_block.delete("all")

        # Starts the new game
        self.start(callback, False)

    def end_turn(self, player: str) -> None:
        # Checks if the player has won
        if check_win(self.grid, player):
            if player == "X":
                # Updates variables
                self.x_score += 1

                self.gui.turn_var.set("X wins!\nPress R to play again.")
                self.gui.x_score_var.set(f"X score:\n{self.x_score}")

                # Ends the game
                self.end_game()
                self.game_over = True
            else:
                # Updates variables
                self.o_score += 1

                self.gui.turn_var.set("O wins!\nPress R to play again.")
                self.gui.o_score_var.set(f"O score:\n{self.o_score}")

                # Ends the game
                self.end_game()
                self.game_over = True

        # Checks if the game is a draw
        elif self.turn_number > 8:
            # Updates variables
            self.x_score += 0.5
            self.o_score += 0.5

            self.gui.turn_var.set("Draw!\nPress R to play again.")
            self.gui.x_score_var.set(f"X score:\n{self.x_score}")
            self.gui.o_score_var.set(f"O score:\n{self.o_score}")

            # Ends the game
            self.end_game()
            self.game_over = True

    def end_game(self) -> None:
        # Places label if hidden
        self.gui.turn_label.place(relx=0.5, rely=0.1, anchor="center")

        # Unbinds the callback function
        for grid_block in self.gui.grid_blocks:
            grid_block.unbind("<Button-1>")

        # Binds new_game function
        self.gui.bind("<r>", lambda e: self.new_game(self.callback))
        self.gui.bind("<R>", lambda e: self.new_game(self.callback))

    def get_player(self) -> str:
        # Returns player based on the turn and game number
        if self.game_number % 2 == 0:
            if self.turn_number % 2 == 0:
                return "X"
            else:
                return "O"
        else:
            if self.turn_number % 2 == 0:
                return "O"
            else:
                return "X"

    def play_move(self, index: int, player) -> None:
        # Gets the grid block
        grid_block = self.gui.grid_blocks[index]

        # Updates the GUI and variables
        self.grid[index] = player
        draw_symbol(player, grid_block)

        self.turn_number += 1

        # Ends the player's turn
        self.end_turn(player)
