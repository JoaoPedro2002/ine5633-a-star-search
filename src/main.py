import search
import time
from src.board import Board
from logger import logger, VERBOSE

if __name__ == "__main__":
    random_board = Board.new_board()
    logger.log(VERBOSE, "Tabuleiro desordenado \n" + Board.board_to_str(random_board))

    # Custo uniforme e tempo para resolver
    start = time.time()
    path = search.uniform_cost_search(random_board)
    end = time.time()
    print(end - start)

    # Constroi o tabuleiro resolvido
    while not path.empty():
        empty_space = Board.board_state(random_board)[1]
        random_board = Board.move(random_board, path.get(), empty_space)
    logger.log(VERBOSE, "Tabuleiro resolvido \n" + Board.board_to_str(random_board))
