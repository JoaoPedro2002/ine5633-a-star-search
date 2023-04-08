from typing import Callable
from array import array

from logger import logger
from queue import Queue, LifoQueue, PriorityQueue

import board_utils

"""
Valores muito significativos podem acarretar no melhor caminho não sendo escolhido.
Mas o tempo de busca é mais rápida que a de custo uniforme
"""
HEURISTIC_WEIGHT = 0.2


class Node:
    def __init__(self, board, parent, move, depth):
        self.board: array[int] = board
        self.parent: Node = parent
        self.move: tuple[int] = move
        self.depth = depth
        self.weight = 0

    def __gt__(self, other):
        return self.weight > other.weight

    def __eq__(self, other):
        return self.weight == other.weight


def uniform_cost_search(board: [int]) -> tuple[Queue[tuple[int, int]], int]:
    """
    Busca de custo uniforme.
    :param board: tabuleiro
    :return: sequencia de movimentos para resolver o tabuleiro enviado
    """
    queue = Queue()
    current = Node(board, None, None, 0)
    visited = set()
    total_visited = 0
    while not board_utils.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_str = "".join(str(item) for item in item.board)
            if board_str in visited: continue
            visited.add(board_str)
            queue.put(item)
        current = queue.get()

    return get_path_from_node(current), total_visited


def a_star_search(board: [int], heuristic: Callable) -> tuple[Queue[tuple[int, int]], int]:
    queue = PriorityQueue()
    current = Node(board, None, None, 0)
    visited = set()
    total_visited = 0
    while not board_utils.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_str = "".join(str(item) for item in item.board)
            if board_str in visited: continue
            visited.add(board_str)
            item.weight = current.weight + heuristic(item)
            queue.put(item)
        current = queue.get()

    return get_path_from_node(current), total_visited


def basic_heuristic(node: Node):
    score = len(board_utils.GOAL)
    for i in range(board_utils.N_ELEMENTS):
        score -= node.board[i] == (i + 1) % board_utils.N_ELEMENTS
    return score * HEURISTIC_WEIGHT


def advanced_heuristic(node: Node):
    score = 0
    for i in range(board_utils.N_ELEMENTS):
        element = node.board[i]
        correct_x, correct_y = divmod((element - 1) % board_utils.N_ELEMENTS, board_utils.N_LINES)
        x, y = divmod(i, board_utils.N_LINES)
        score += ((x - correct_x) ** 2 + (y - correct_y) ** 2) ** 0.5
    return score * HEURISTIC_WEIGHT


def get_path_from_node(node: Node) -> Queue[tuple[int, int]]:
    path = LifoQueue(node.depth)
    while node.parent is not None:
        path.put(node.move)
        node = node.parent
    return path


def children(node) -> list[Node]:
    moves, empty_space = board_utils.board_state(node.board)
    nodes = [Node(board_utils.move(node.board, move, empty_space),
                  node, move, node.depth + 1) for move in moves]
    logger.debug(f"Found {len(nodes)} children at depth {node.depth} for parent {node}")
    return nodes
