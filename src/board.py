import random

class Board:
    N_LINES = 3
    N_ELEMENTS = N_LINES**2
    GOAL = [*range(1, N_ELEMENTS), 0]
    @staticmethod
    def new_board(number_of_moves=10*N_ELEMENTS) -> list[list[int]]:
        """
        O método constrói um tabuleiro ordenado e realiza movimentos aleatórios.
        O método não trata movimentos redundantes
        :param number_of_moves: número de movimentos que serão realizados
        :return: tabuleiro
        """
        numbers = Board.GOAL[:]
        board = list()
        for _ in range(Board.N_LINES):
            board.append([[0]] * Board.N_LINES)

        for i in range(Board.N_LINES):
            for j in range(Board.N_LINES):
                value = numbers[i * Board.N_LINES + j]
                board[i][j] = value

        for i in range(number_of_moves):
                state = Board.board_state(board)
                move = random.choice(state[0])
                board = Board.move(board, move, state[1])

        return board

    @staticmethod
    def game_is_over(board: list[list[int]]) -> bool:
        """
        Compara o tabuleiro enviado com o objetivo
        :param board: tabuleiro
        :return: se o objetivo foi alcançado
        """
        return Board.flatten(board) == Board.GOAL

    @staticmethod
    def board_to_str(board: list[list[int]]) -> str:
        """
        Retorna o tabuleiro como string
        :param board:
        :return: tabuleiro como str formatado
        """
        s = [[str(e) for e in row] for row in board]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)

    @staticmethod
    def move(board, move: tuple[int, int], empty_space: tuple[int, int]) -> list[list[int]]:
        """
        Realiza um movimento e retorna o novo tabuleiro
        :param board: tabuleiro
        :param move: movimento
        :param empty_space: coordenadas do espaço vazio
        :return: novo tabuleiro
        """
        new_board = board[:]
        for i in range(Board.N_LINES):
            new_board[i] = new_board[i][:]
        new_board[empty_space[0]][empty_space[1]] = new_board[move[0]][move[1]]
        new_board[move[0]][move[1]] = 0
        return new_board

    @staticmethod
    def board_state(board: list[list[int]],
                    last_move: tuple[int, int]=None) -> tuple[list[tuple[int, int]], tuple[int, int]]:
        """
        Retorna o estado do tabuleiro
        :param board:
        :param last_move:
        :return: tupla contendo movimentos possíveis e a posição vazia
        """
        empty_pos = Board.get_empty_pos(board)
        board_x_axis = empty_pos[0]
        board_y_axis = empty_pos[1]

        possible_moves = list()
        if board_x_axis > 0:
            possible_moves.append((board_x_axis - 1, board_y_axis))
        if board_x_axis + 1 < Board.N_LINES:
            possible_moves.append((board_x_axis + 1, board_y_axis))
        if board_y_axis > 0:
            possible_moves.append((board_x_axis, board_y_axis - 1))
        if board_y_axis + 1 < Board.N_LINES:
            possible_moves.append((board_x_axis, board_y_axis + 1))
        if last_move:
            possible_moves.remove(last_move)
        return possible_moves, empty_pos

    @staticmethod
    def get_empty_pos(board):
        for i in range(Board.N_LINES):
            for j in range(Board.N_LINES):
                if board[i][j] == 0:
                    return i, j

    @staticmethod
    def flatten(board: list[list[int]]) -> list[int]:
        """
        Transforma uma matriz em uma lista
        :param board: tabuleiro
        :return: lista
        """
        function = lambda x: x
        flat_map = lambda func, matrix: [n for line in matrix for n in func(line)]
        return flat_map(function, board)