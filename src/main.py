import search
import time
from src.board import Board
from logger import logger, VERBOSE

def measure_search(search_function, board: list[list[int]], advanced = False):
    start = time.time()
    result = search_function(board, advanced) if advanced else search_function(board)
    end = time.time()
    logger.log(VERBOSE, f"Tempo: {end-start} para {search_function.__name__}")
    return result


def build_board(smallest_path, board):
    while not smallest_path.empty():
        empty_space = Board.board_state(board)[1]
        board = Board.move(board, smallest_path.get(), empty_space)
    logger.log(VERBOSE, "Tabuleiro resolvido \n" + Board.board_to_str(board))


if __name__ == "__main__":
    # Easier board solvable in 6 moves:  [[2, 5, 3], [1, 0, 6], [4, 7, 8]]
    # Medium board solvable in 14 moves: [[2, 3, 8], [1, 0, 6], [5, 4, 7]]
    # Harder board solvable in 26 moves: [[6, 3, 7], [4, 0, 8], [1, 2, 5]]
    random_board = Board.new_board()
    logger.log(VERBOSE, "Tabuleiro desordenado \n" + Board.board_to_str(random_board))
    path = measure_search(search.a_star_search, random_board)
    # measure_search(search.uniform_cost_search, random_board)
    build_board(path, random_board)
