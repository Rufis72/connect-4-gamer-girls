import copy

class Board:
    def __init__(self):
        self.board = [[None] * 6] * 7
        self.turn = True # true is red, false is yellow

    def get_possible_moves(self) -> list[int]:
        '''Returns a list of all possible columns that could be played in. (They are numbered, 0 is leftmost, 6 is rightmost)'''
        possible_moves = []
        # going through all the columns
        for column in range(7):
            # checking if the top spot of the column is taken
            if self.board[column][5] == None:
                # adding that column to the list of possible moves, since it's still got space
                possible_moves.append(column)
        # returning all the possible moves
        return possible_moves

    def copy(self):
        '''Returns a copy of self'''
        return copy.deepcopy(self)

    def minimax(self, depth: int, who_minimaxing_for: bool) -> tuple[int, int]:
        '''Searches all possible moves, and choose the best one for the player mini-maxing for.

        If depth == 0: Then it returns the evaluation of the position gotten from self.eval()
        The evaluation is just if one player has won. 0 is tie, 1 is red, -1 is yellow
        Otherwise, it chooses the best evaluation from all of its child positions, and returns that.

        Returns a tuple of A. the move made, and B. it's evaluation'''
        # if depth is 0, returning the evaluation of the function
        if depth == 0:
            return self.eval()

        # since we haven't reached max depth, we find the best move
        # we do this by calling minimax on all the possible moves from the current board state
        # what we technically do is deepcopy this board state, then make all the possible moves from there.
        # then we'll return the evaluation for the best move, and that best move
        # we split up based off the player we're evaluating for, since if it were combined, it'd be slower, and harder to read
        if who_minimaxing_for: # this is for red
            # defining variables
            best_move = None
            best_move_eval = -2 # this is negative 2, since the worst you could get would be -1, guaranteeing we'll get a real move, instead of this placeholder one
            # for red, we like higher evaluations better

            # this is where we specifically go through, and evaluate every move
            for move in self.get_possible_moves():
                move_we_are_evaluating_board = self.copy()
                # making the move
                move_we_are_evaluating_board.move(move)
                evaluation_result = move_we_are_evaluating_board.minimax(depth - 1, not who_minimaxing_for)
                # updating the best move if it's better than our previous best move
                if evaluation_result[1] > best_move_eval:
                    best_move = move
                    best_move_eval = evaluation_result[1]

            # returning the best move
            return (best_move, best_move_eval)

        else: # this is for yellow
            # defining variables
            best_move = None
            best_move_eval = 2  # this is 2, since the worst you could get would be 1, guaranteeing we'll get a real move, instead of this placeholder one
            # for yellow, we like the lowest number for the evaluation

            # this is where we specifically go through, and evaluate every move
            for move in self.get_possible_moves():
                move_we_are_evaluating_board = self.copy()
                # making the move
                move_we_are_evaluating_board.move(move)
                evaluation_result = move_we_are_evaluating_board.minimax(depth - 1, not who_minimaxing_for)
                # updating the best move if it's better than our previous best move
                if evaluation_result[1] < best_move_eval:
                    best_move = move
                    best_move_eval = evaluation_result[1]

            # returning the best move
            return (best_move, best_move_eval)

    def eval(self) -> tuple[None, int]:
        '''Evaluates the position.

        Returns a tuple where the first one is always None (this is for minimax stuff), and the second is the evaluation
        If the second number is 1, it means red won, -1 means yellow won, and 0 means nobody's won yet.'''
        return (None, 0)

    def move(self, column: int):
        '''Plays a piece in the specified column'''
        # checking until we find an empty spot
        for row, piece in enumerate(self.board[column]):
            # checking if this spot is empty
            if piece == None:
                # putting a piece in the formerly empty spot
                self.board[column][row] = self.turn
                # changing whose turn it is
                self.turn = not self.turn
                # ending the loop
                return None
print(Board().minimax(2, False))