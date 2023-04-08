from typing import Callable

from logger import logger
from queue import Queue, LifoQueue, PriorityQueue

from src.board import Board

"""
Valores muito significativos podem acarretar no melhor caminho não sendo escolhido.
Mas o tempo de busca é mais rápida que a de custo uniforme
"""
HEURISTIC_WEIGHT = 0.2

class Node:
    def __init__(self, board, parent, move, depth):
        self.board: list[list[int]] = board
        self.parent: Node = parent
        self.move: tuple[int] = move
        self.depth = depth
        self.weight = 0

    def __gt__(self, other):
        return self.weight > other.weight

    def __eq__(self, other):
        return self.weight == other.weight


def uniform_cost_search(board: list[list[int]]) -> tuple[Queue[tuple[int, int]], int]:
    """
    Busca de custo uniforme.
    :param board: tabuleiro
    :return: sequencia de movimentos para resolver o tabuleiro enviado
    """
    queue = Queue()
    current = Node(board, None, None, 0)
    visited = set()
    total_visited = 0
    while not Board.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_str = "".join(["".join([str(i) for i in line]) for line in item.board])
            if board_str in visited: continue
            visited.add(board_str)
            queue.put(item)
        current = queue.get()

    return get_path_from_node(current), total_visited


def a_star_search(board: list[list[int]], heuristic: Callable) -> tuple[Queue[tuple[int, int]], int]:
    queue = PriorityQueue()
    current = Node(board, None, None, 0)
    visited = set()
    total_visited = 0
    while not Board.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_str = "".join(["".join([str(i) for i in line]) for line in item.board])
            if board_str in visited: continue
            visited.add(board_str)
            item.weight = current.weight + heuristic(item)
            queue.put(item)
        current = queue.get()

    return get_path_from_node(current), total_visited


def basic_heuristic(node: Node):
    score = len(Board.GOAL)
    for i in range(Board.N_LINES):
        for j in range(Board.N_LINES):
            score -= node.board[i][j] == ((i*Board.N_LINES + j + 1) % Board.N_ELEMENTS)
    return score * HEURISTIC_WEIGHT


def advanced_heuristic(node: Node):
    score = 0
    for x in range(Board.N_LINES):
        for y in range(Board.N_LINES):
            element = node.board[x][y]
            correct_x, correct_y = divmod((element - 1) % Board.N_ELEMENTS, Board.N_LINES)
            # Distancia entre as coordenadas atuais de um elemento e as corretas
            score += ((x - correct_x) ** 2 + (y - correct_y) ** 2) ** 0.5
    return score * HEURISTIC_WEIGHT


def get_path_from_node(node: Node) -> Queue[tuple[int, int]]:
    path = LifoQueue()
    while node.parent is not None:
        path.put(node.move)
        node = node.parent
    return path


def children(node) -> list[Node]:
    moves, empty_space = Board.board_state(node.board)
    nodes = [Node(Board.move(node.board, move, empty_space),
                  node, move, node.depth + 1) for move in moves]
    logger.debug(f"Found {len(nodes)} children at depth {node.depth} for parent {node}")
    return nodes
