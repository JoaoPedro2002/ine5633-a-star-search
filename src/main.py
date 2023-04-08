from typing import Callable

import search
import time

from src.board import Board
from logger import logger, VERBOSE, set_level

"""
Modificar valor para enriquecer os logs
VERBOSE: tempo, numero de nodos e movimentos
INFO: tudo acima mais o tabuleiro
DEBUG: tudo acima mais informações da busca
"""
LOG_LEVEL = VERBOSE # VERBOSE, 'INFO' ou 'DEBUG'


def measure_search(search_function: Callable, func_args: tuple):
    logger.log(VERBOSE, f"Testing {str(search_function.__name__).upper()} with args {func_args}")
    start = time.time()
    path, total_visited = search_function(*func_args)
    end = time.time()
    logger.log(VERBOSE, f"Number of moves: {path.qsize()}")
    logger.log(VERBOSE, f"Visited: {total_visited} nodes")
    logger.log(VERBOSE, f"Time: {end - start} for {str(search_function.__name__).upper()}")
    return path


def build_board(smallest_path, board):
    while not smallest_path.empty():
        empty_space = Board.board_state(board)[1]
        board = Board.move(board, smallest_path.get(), empty_space)
    return board


def measure_algorithm(search_function: Callable, func_args: tuple):
    logger.info("Unordered board \n" + Board.board_to_str(func_args[0]))
    path = measure_search(search_function, func_args)
    ordered_board = build_board(path, func_args[0])
    logger.info("Ordered board \n" + Board.board_to_str(ordered_board))


if __name__ == "__main__":
    set_level(LOG_LEVEL)
    # Easier board solvable in 06 moves: [[2, 5, 3], [1, 0, 6], [4, 7, 8]]
    # Medium board solvable in 14 moves: [[2, 3, 8], [1, 0, 6], [5, 4, 7]]
    # Harder board solvable in 26 moves: [[6, 3, 7], [4, 0, 8], [1, 2, 5]]
    random_board = Board.new_board()
    measure_algorithm(search.uniform_cost_search, (random_board[:],))
    measure_algorithm(search.a_star_search, (random_board[:], search.basic_heuristic))
    measure_algorithm(search.a_star_search, (random_board[:], search.advanced_heuristic))
