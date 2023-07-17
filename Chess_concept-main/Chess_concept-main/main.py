import Counter
import collections
import chess
import chess.engine
import chess.pgn
import numpy as np
import random
import time


class AlphaZeroChess:
    def __init__(self):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\dania\OneDrive\Документы\stockfish_15.1_win_x64_popcnt")

    def play_game(self):
        game = chess.pgn.Game()
        game.headers["Event"] = "AlphaZero vs AlphaZero"
        game.headers["Site"] = "Somewhere"
        game.setup(self.board.fen())

        while not self.board.is_game_over():
            if self.board.turn == chess.WHITE:
                move = self.alpha_zero_search()
            else:
                move = self.alpha_zero_search()

            self.board.push(move)
            game.add_variation(move)

        print(game, file=open("game.pgn", "w"), end="\n\n")
        self.engine.quit()

    def alpha_zero_search(self, timeout=10.0):
        state = self.get_state()
        root = Node(state)
        start = time.time()

        while time.time() - start < timeout:
            leaf = self.select(root)
            value = self.evaluate(leaf.state)
            self.backup(leaf, value)

        return self.choose_move(root)

    def get_state(self):
        state = np.zeros((8, 8, 5), dtype=np.int8)

        for i in range(8):
            for j in range(8):
                piece = self.board.piece_at(chess.square(i, j))
                if piece is not None:
                    index = {
                        chess.PAWN: 0,
                        chess.KNIGHT: 1,
                        chess.BISHOP: 2,
                        chess.ROOK: 3,
                        chess.QUEEN: 4,
                        chess.KING: 5,
                    }[piece.piece_type]
                    sign = -1 if piece.color == chess.BLACK else 1
                    state[i][j][index] = sign

        if self.board.turn == chess.BLACK:
            state = np.rot90(state, k=2, axes=(0, 1))

        return state

    def select(self, node):
        while node.is_expanded():
            node = node.select_child()
        return node.expand()

    def evaluate(self, state):
        pass  # TODO: Implement evaluation function

    def backup(self, node, value):
        while node is not None:
            node.visits += 1
            node.value_sum += value
            node = node.parent

    def choose_move(self, root):
        visit_counts = [child.visits for child in root.children]
        best_child = np.random.choice(
            np.flatnonzero(visit_counts == visit_counts.max())
        )
        return root.children[best_child].move


class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value_sum = 0

    def is_expanded(self):
        return len(self.children) > 0

    def select_child(self):
        total_visits = sum(child.visits for child in self.children)
        log_visits = np.log(total_visits)

        def ucb_score(child):
            exploration_factor = 1.0
            exploitation_factor = child.value_sum / child.visits
            exploration_term = exploration_factor * np.sqrt(
                log_visits / child.visits
            )