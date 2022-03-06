import random
import math

BOT_NAME = "Boogie_Woogie_Bot_Boi_383"

class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None
        
        for move, state in state.successors():
            util = self.minimax(state)
            # print("nextp:", nextp, "| util:", util, "| best_util:", best_util)

            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        # If state is terminal state, return it's utility
        if (state.is_full()):
            return state.utility()

        # Recurse through minimax
        if state.next_player() == 1:
            v = -math.inf
            for m, s in state.successors():
                util = self.minimax(s)
                v = max(v, util)
            return v
        else:
            v = math.inf
            for m, s in state.successors():
                util = self.minimax(s)
                v = min(v, util)
            return v


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  
        
        If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  
        
        If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        if (self.depth_limit == None): # If depth_limit is None, traverse whole tree
            return MinimaxAgent.minimax(state)
        else: # Otherwise, traverse tree with depth_limit
            return self.minimax_depth(state, self.depth_limit)

    def minimax_depth(self, state, depth):
        """This is just a helper method for minimax(). Feel free to use it or not. """
        if (depth > 0): # While depth is greater than 0,
            if (state.is_full()): # If terminal state, return utility value
                return state.utility()
            
            if state.next_player() == 1: # Traverse tree while decrementing depth by 1
                v = -math.inf
                for m, s in state.successors():
                    util = self.minimax_depth(s, depth-1)
                    v = max(v, util)
                return v
            else:
                v = math.inf
                for m, s in state.successors():
                    util = self.minimax_depth(s, depth-1)
                    v = min(v, util)
                return v

        else: # If depth is zero,
            if (state.is_full()): # If state is terminal, return utility value
                return state.utility()
            else: # Otherwise, return evaluation of state
                return self.evaluation(state)

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """
        cols_list = state.get_cols() # List of columns of game state
        rows_list = state.get_rows() # List of rows of game state
        diag_list = state.get_diags() # List of diagonals of game state

        # Total streak point counters for entire search
        p1_total_streak = 0
        p2_total_streak = 0
        
        # Current streak counters while searching through rows, cols and diags
        p1_curr_streak = 0
        p2_curr_streak = 0

        # Counters for number of P1's, P2's and space marks on a given row, column or diagonal
        p1_counter = 0
        p2_counter = 0
        # space_counter = 0

        # Going through all rows, columns and diagonals of board
        for i in cols_list + rows_list + diag_list:
            for j in range(len(i)):
                if i[j] == 1: # If location is P1's mark,
                    if p2_curr_streak >= 3: # Check P2's current streak
                        p2_total_streak += p2_curr_streak**2 # Update P2's total streak if needed
                    p2_curr_streak = 0 # Reset P2's current streak
                    p1_curr_streak += 1 # Increment P1's streak
                    p1_counter += 1 # Increment P1 count
                
                elif i[j] == -1: # If location is P2's mark,
                    if p1_curr_streak >= 3: # Check P1's current streak
                        p1_total_streak += p1_curr_streak**2 # Update P1's total streak if needed
                    p1_curr_streak = 0 # Reset P1's current streak
                    p2_curr_streak += 1 # Increment P2's streak
                    p2_counter += 1 # Increment P2 count

                elif i[j] == 0: # If location is blank space,
                    if p1_curr_streak > 0: # If we are counting P1's current streak,
                        p1_curr_streak += 1 # Increment P1's curr streak
                    elif p2_curr_streak > 0: # If we are counting P2's current streak,
                        p2_curr_streak += 1 # Increment P2's curr streak
                    else: # If we do not know whose streak we are currently counting,
                        if state.next_player() == 1: # If it is P1's turn,
                            p1_curr_streak += 1 # Increment P1's curr streak
                        else: # Otherwise, 
                            p2_curr_streak += 1 # Increment P2's curr streak
                    # space_counter += 1 # Increment space counter
                        
                else: # If location is neither P1 or P2 (either empty space or blocked)
                    if p1_curr_streak >= 3: # Check P1's current streak
                        p1_total_streak += p1_curr_streak**2 # Update P1's total streak if needed
                    p1_curr_streak = 0 # Reset P1's current streak

                    if p2_curr_streak >= 3: # Check P2's current streak
                        p2_total_streak += p2_curr_streak**2 # Update P2's total streak if needed
                    p2_curr_streak = 0 # Reset P2's current streak
            
            # After going through a whole column, row or diagonal, 
            # we predict how many possible/futuristic combinations we could get
            if p1_counter > p2_counter:
                p1_total_streak += p1_counter**2
            elif p1_counter < p2_counter:
                p2_total_streak += p2_counter**2
            
            # Reset counters
            p1_counter = 0
            p2_counter = 0
            # space_counter = 0
        
        # Return difference between total P1 and P2 streaks
        return p1_total_streak - p2_total_streak


class MinimaxPruneAgent(MinimaxAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move.
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.
        
        You can check this by inspecting the value of the class variable GameState.state_count, 
        which keeps track of how many GameState objects have been created over time. 
        
        This agent should ignore any depth limits like HeuristicAgent.

        N.B.: 
        When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  
        
        That is, you cannot prune the state reached by moving to column 4 before you've 
        explored the state reached by a move to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        return self.alphabeta(state, -math.inf, math.inf)

    def alphabeta(self, state, alpha, beta):
        """ This is just a helper method for minimax(). Feel free to use it or not. """
        # return 9 # change this line!
        # If state is terminal state, return it's utility value
        if (state.is_full()):
            return state.utility()

        # Recurse through minimax
        if state.next_player() == 1:
            v = -math.inf
            for m, s in state.successors():
                util = self.alphabeta(s, alpha, beta)
                v = max(v, util)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        else:
            v = math.inf
            for m, s in state.successors():
                util = self.minimax(s)
                v = min(v, util)
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v


class OtherMinimaxHeuristicAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    """This is normal minimax agent; used to compare to Heuristic and Pruning"""
    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None
        
        for move, state in state.successors():
            util = self.minimax(state)
            # print("nextp:", nextp, "| util:", util, "| best_util:", best_util)

            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        # If state is terminal state, return it's utility
        if (state.is_full()):
            return state.utility()

        # Recurse through minimax
        if state.next_player() == 1:
            v = -math.inf
            for m, s in state.successors():
                util = self.minimax(s)
                v = max(v, util)
            return v
        else:
            v = math.inf
            for m, s in state.successors():
                util = self.minimax(s)
                v = min(v, util)
            return v