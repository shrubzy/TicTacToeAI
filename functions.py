from customtkinter import CTkCanvas


def check_win(grid: list, player: str) -> bool:
    if (
            # Row wins
            grid[0] == grid[1] == grid[2] == player or
            grid[3] == grid[4] == grid[5] == player or
            grid[6] == grid[7] == grid[8] == player or

            # Column wins
            grid[0] == grid[3] == grid[6] == player or
            grid[1] == grid[4] == grid[7] == player or
            grid[2] == grid[5] == grid[8] == player or

            # Diagonal Wins
            grid[0] == grid[4] == grid[8] == player or
            grid[2] == grid[4] == grid[6] == player
    ):
        return True
    return False


def draw_symbol(player: str, grid_block: CTkCanvas) -> None:
    if player == "X":
        grid_block.create_line(15, 15, 135, 135, width=5, fill="#9A208C")
        grid_block.create_line(15, 135, 135, 15, width=5, fill="#9A208C")
    elif player == "O":
        grid_block.create_oval(15, 15, 135, 135, width=5, outline="#9A208C")
