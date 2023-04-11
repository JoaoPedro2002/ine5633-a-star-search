import random
from array import array
from functools import wraps

N_LINES = 3
N_ELEMENTS = N_LINES ** 2
GOAL: [int] = array('B', [*range(1, N_ELEMENTS), 0])


def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = args[0]
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key].copy()
    return wrapper


def new_board(number_of_moves=30 * N_LINES) -> [int]:
    """
    O método constrói um tabuleiro ordenado e realiza movimentos aleatórios.
    O método não trata movimentos redundantes
    :param number_of_moves: número de movimentos que serão realizados
    :return: tabuleiro
    """
    board = GOAL[:]
    for i in range(number_of_moves):
        state = board_state(board)
        chosen_move = random.choice(tuple(state[0]))
        board = move(board, chosen_move, state[1])

    return board


def game_is_over(board: [int]) -> bool:
    """
    Compara o tabuleiro enviado com o objetivo
    :param board: tabuleiro
    :return: se o objetivo foi alcançado
    """
    return board == GOAL


def board_to_str(board: [int]) -> str:
    """
    Retorna o tabuleiro como string
    :param board:
    :return: tabuleiro como str formatado
    """
    board_copy = board[:]
    board_2d = []
    while board_copy:
        board_2d.append(board_copy[:N_LINES])
        board_copy = board_copy[N_LINES:]

    s = [[str(e) for e in row] for row in board_2d]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)


def move(board: [int], chosen_move: int, empty_space: int) -> list[int]:
    """
    Realiza um movimento e retorna o novo tabuleiro
    :param board: tabuleiro
    :param chosen_move: movimento
    :param empty_space: coordenadas do espaço vazio
    :return: novo tabuleiro
    """
    board_copy = board[:]
    board_copy[empty_space] = board_copy[chosen_move]
    board_copy[chosen_move] = 0
    return board_copy


def board_state(board: [int]) -> tuple[set[int], int]:
    """
    Retorna o estado do tabuleiro
    :param board:
    :return: tupla contendo movimentos possíveis e a posição vazia
    """
    empty_pos = get_empty_pos(board)
    moves = possible_moves(empty_pos)
    return moves, empty_pos


@memoize
def possible_moves(empty_pos):
    moves: set[int] = {
        empty_pos + (N_LINES * (empty_pos + N_LINES < N_ELEMENTS)),
        empty_pos - (N_LINES * (empty_pos - N_LINES >= 0)),
        empty_pos + (empty_pos % N_LINES != N_LINES - 1),
        empty_pos - (empty_pos % N_LINES != 0)
    }
    moves.discard(empty_pos)
    return moves


def get_empty_pos(board: [int]) -> int:
    return board.index(0)