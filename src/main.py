import search
import time
from src.board import Board

if __name__ == "__main__":
    easy_board = [[1,2,3], [None,5,6], [4,7,8]]
    random_board = Board.new_board()
    Board.pretty_print(random_board)

    # Custo uniforme e tempo para resolver
    start = time.time()
    path = search.uniform_cost_search(random_board)
    end = time.time()
    print(end - start)

    # Constroi o tabuleiro resolvido
    while not path.empty():
        empty_space = Board.board_state(random_board)[1]
        random_board = Board.move(random_board, path.get(), empty_space)
    Board.pretty_print(random_board)
