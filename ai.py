from functions import check_win
from random import choice
from math import inf


class AI:
    def __init__(self, player: str) -> None:
        # Initialise variables
        self.player = player
        self.opponent = "O" if self.player == "X" else "X"
        self.steps = 0

    def score_move(self, grid: list, is_maximising: bool, alpha: float = -inf, beta: float = inf) -> int:
        self.steps += 1

        possible_moves = [value for value in grid if isinstance(value, int)]

        # Score move based on game outcome
        if check_win(grid, self.player):
            return 1

        if check_win(grid, self.opponent):
            return -1

        if len(possible_moves) == 0:
            return 0

        if is_maximising:
            best = -inf

            for index in possible_moves:
                grid[index] = self.player  # 'Play' this move
                score = self.score_move(grid, False, alpha, beta)  # Recursively score move
                grid[index] = index  # Reset grid prior to move

                # Pruning
                best = max(best, score)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best

        else:
            best = inf

            for index in possible_moves:
                grid[index] = self.opponent  # 'Play' this move
                score = self.score_move(grid, True, alpha, beta)  # Recursively score move
                grid[index] = index  # Reset grid prior to move

                # Pruning
                best = min(best, score)
                beta = min(beta, best)

                if beta <= alpha:
                    break

            return best

    def get_best_move(self, grid: list) -> int | None:
        possible_moves = [element for element in grid if isinstance(element, int)]

        moves = []

        best_score = -inf

        for index in possible_moves:
            grid[index] = self.player
            score = self.score_move(grid, False)  # Score every possible move
            grid[index] = index

            move = {"index": index, "score": score, "steps": self.steps}
            moves.append(move)

            self.steps = 0

            best_score = max(score, best_score)

        best_moves = [move for move in moves if move["score"] == best_score]  # Get moves with best score

        if best_moves:

            # If able to win on next move, return that move's index
            instant_wins = [move for move in best_moves if move["steps"] == 1]
            if instant_wins:
                return choice(instant_wins)["index"]

            # Otherwise a random choice from the best moves
            return choice(best_moves)["index"]

    def get_normal_move(self, grid: list) -> int:
        possible_moves = [value for value in grid if isinstance(value, int)]

        for index in possible_moves:
            grid[index] = self.player

            # If able to win on next move, return that move's index
            if check_win(grid, self.player):
                return index

            grid[index] = index

        for index in possible_moves:
            grid[index] = self.opponent

            # If opponent is able to win on next move, return that move's index
            if check_win(grid, self.opponent):
                return index

            grid[index] = index

        # Otherwise return random move
        return choice(possible_moves)
