"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from math import log

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    # identify if player is first player
    if game._player_1 == player:
        # go away from opponent but stay closer to the center
        opp_location = game.get_player_location(game.get_opponent(player))
        center_location = (int(game.height/2), int(game.width/2))
        my_location = game.get_player_location(player)

        my_available_moves = len(game.get_legal_moves(player))

        if opp_location is None:
            opp_location = (-1,-1)

        my_dist = log(1+abs(my_location[0]-center_location[0]) + abs(my_location[1]-center_location[1]))
        opp_dist = log(1+abs(opp_location[0]-center_location[0]) + abs(opp_location[1]-center_location[1]))
        dist_to_opp = log(abs(opp_location[0]-my_location[0]) + abs(opp_location[1]-my_location[1]))

        score = 3*my_available_moves + opp_dist - my_dist + dist_to_opp

    else:
        # get close to the opponent and block him
        game_state = len(game.get_blank_spaces())/(game.height*game.width)

        my_available_moves = len(game.get_legal_moves(player))
        opponent_available_moves = len(game.get_legal_moves(game.get_opponent(player)))
        score = my_available_moves - 4*game_state*opponent_available_moves

    return score


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    # Get further from the opponent, but favour positions which have more
    # available moves
    # Weight available moves by Manhattan distance between opponent
    # This is initial 'unweighted' score function

    game_state = len(game.get_blank_spaces())/(game.height*game.width)

    my_available_moves = len(game.get_legal_moves(player))
    opponent_available_moves = len(game.get_legal_moves(game.get_opponent(player)))
    score = my_available_moves - 4*game_state*opponent_available_moves

    return score


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------F
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    # Get further from the opponent, but favour positions which have more
    # available moves more as the game progresses
    # Weight available moves by Manhattan distance between opponent

    opp_location = game.get_player_location(game.get_opponent(player))
    center_location = (int(game.height/2), int(game.width/2))
    my_location = game.get_player_location(player)

    my_available_moves = len(game.get_legal_moves(player))

    if opp_location is None:
        opp_location = (-1,-1)

    my_dist = log(1+abs(my_location[0]-center_location[0]) + abs(my_location[1]-center_location[1]))
    opp_dist = log(1+abs(opp_location[0]-center_location[0]) + abs(opp_location[1]-center_location[1]))
    dist_to_opp = log(abs(opp_location[0]-my_location[0]) + abs(opp_location[1]-my_location[1]))

    score = 3*my_available_moves + opp_dist - my_dist + dist_to_opp

    return score


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=30.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move   

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # TODO: finish this function!

        def minimax_decision(self, game, depth):
            """Top level function which calls min_value and this way produces
            recursive evaluation process. After wheights are propagated using minmax
            it returns best move based on scores"""
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            v = (float("-inf"), (-1,-1))
            for move in game.get_legal_moves():
                # For each available move calculate scores
                v = max(v, (min_value(self, game.forecast_move(move), depth-1), move))
            # Return element with highest score or if there are no available moves
            # return (-1,-1)
            return v[1]

        def max_value(self, game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If lowest level is reached, then return score of active player,
            # since it is initial agent.
            if depth==0:
                return self.score(game, self)
            if (len(game.get_legal_moves()) == 0):
                return game.utility(self)
            v = float("-inf")
            # for every available move call min_value, thus producing recursion
            for move in game.get_legal_moves():
                # update v value if it is higher than the current one
                v = max(v, min_value(self, game.forecast_move(move), depth-1))
            return v

        def min_value(self, game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If lowest level is reached, then return score of inactive player,
            # since it is initial agent.
            if depth==0:
                return self.score(game, self)
            if (len(game.get_legal_moves(game.get_opponent(self))) == 0):
                return game.utility(self)
            v = float("inf")
            # for every available move call max_value, thus producing recursion
            for move in game.get_legal_moves(game.get_opponent(self)):
                # update v value if it is higher than the current one
                v = min(v, max_value(self, game.forecast_move(move), depth-1))
            return v

        # call minimax_decision to get best move
        return minimax_decision(self, game, depth)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        # TODO: finish this function!

        # seting nitial variables
        depth = 1
        best_move = (-1,-1)
        # upper bound of moves left till game end - does not pass test, but might save some resources
        # >>> state = int(len(game.get_blank_spaces())/2)

        try:
            # repeat the process until exception (SearchTimeout)
            # is met and then return best move
            while True:
                # calculate new best move
                new_best_move = self.alphabeta(game, depth)
                # increase depth
                depth += 1
                # if new best move is valid (not equal to (-1,-1))
                # then update best move to it

                # depth does not exceed current state - does not pass test, but might save some resources
                # >>> if (new_best_move != (-1,-1)) and (depth <= state):
                if (new_best_move != (-1,-1)):
                    best_move = new_best_move
                else:
                    return best_move
        except SearchTimeout:
            return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        # Top level function which return
        def alpha_beta_search(self, game, depth, alpha, beta):
            """Top level function which calls min_value and this way produces
            recursive evaluation process. After wheights are propagated using minmax
            and alpha beta pruning it returns best move based on scores"""
            # if self.time_left() < self.TIMER_THRESHOLD:
            #     raise SearchTimeout()
            v = (float("-inf"), (-1,-1))
            for move in game.get_legal_moves():
                # For each available move calculate scores
                v = max(v, (min_value(self, game.forecast_move(move), depth-1, alpha, beta), move))
                if v[0]>=beta:
                    return v[1]
                # update alpha
                alpha = max(alpha, v[0])         
            # Return element with highest score or if there are no available moves
            # return (-1,-1)
            return v[1]

        def max_value(self, game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If lowest level is reached, then return score of active player,
            # since it is initial agent.
            if depth == 0:
                return self.score(game, self)
            if (len(game.get_legal_moves()) == 0):
                return game.utility(self)
            v = float("-inf")
            # for every available move call min_value, thus producing recursion
            for move in game.get_legal_moves():
                v = max(v, min_value(self, game.forecast_move(move), depth-1, alpha, beta))
                # if score is greater then beta there is no point to calculate further and 
                # v can be returned as current score
                if v>=beta:
                    return v
                # update alpha
                alpha = max(alpha, v)
            return v

        def min_value(self, game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # If lowest level is reached, then return score of inactive player,
            # since it is initial agent.
            if depth == 0:
                return self.score(game, self)
            if (len(game.get_legal_moves(game.get_opponent(self))) == 0):
                return game.utility(self)
            v = float("inf")
            # for every available move call max_value, thus producing recursion
            for move in game.get_legal_moves(game.get_opponent(self)):
                v = min(v, max_value(self, game.forecast_move(move), depth-1,  alpha, beta))
                # if score is less then alpha there is no point to calculate further and 
                # v can be returned as current score
                if v <= alpha:
                    return v
                # update beta
                beta = min(beta, v)
            return v

        # call alpha_beta_search to get best move
        return alpha_beta_search(self, game, depth, alpha, beta)




