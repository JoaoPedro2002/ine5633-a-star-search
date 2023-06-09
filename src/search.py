from typing import Callable
from array import array
import hashlib
import heapq

from queue import Queue, LifoQueue

import board_utils


class Node:
    def __init__(self, board, parent, move, depth):
        self.board: array[int] = board
        self.parent: Node = parent
        self.move: int = move
        self.depth = depth
        self.cumulative_weight = 0
        self.weight = 0

    def __gt__(self, other):
        return self.cumulative_weight > other.cumulative_weight

    def __eq__(self, other):
        return self.board == other.board

    def __str__(self):
        return f"Node<depth: {self.depth}, weight: {self.cumulative_weight}>"


def uniform_cost_search(board: [int]) -> tuple[Queue[tuple[int, int]], int]:
    """
    Busca de custo uniforme.
    :param board: tabuleiro
    :return: sequencia de movimentos para resolver o tabuleiro enviado
    """
    queue = Queue()
    current = Node(board, None, board_utils.get_empty_pos(board), 0)
    visited = set()
    total_visited = 0
    while not board_utils.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_hash = hashlib.md5(item.board).digest()
            if board_hash in visited: continue
            visited.add(board_hash)
            queue.put(item)
        current = queue.get()

    return get_path_from_node(current), total_visited


def a_star_search(board: [int], heuristic: Callable[[Node], float]) -> tuple[Queue[tuple[int, int]], int]:
    heap = []
    current = Node(board, None, board_utils.get_empty_pos(board), 0)
    visited = set()
    total_visited = 0
    while not board_utils.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_hash = hashlib.md5(item.board).digest()
            if board_hash in visited: continue
            visited.add(board_hash)
            item.cumulative_weight = current.cumulative_weight + heuristic(item)
            heapq.heappush(heap, (item.cumulative_weight, item))
        current = heapq.heappop(heap)[1]

    return get_path_from_node(current), total_visited


def basic_heuristic(node: Node):
    score = len(board_utils.GOAL)
    for i in range(board_utils.N_ELEMENTS):
        score -= node.board[i] == (i + 1) % board_utils.N_ELEMENTS
    return score


def manhattan_distance(element: int, position: int):
    correct_x, correct_y = divmod((element - 1) % board_utils.N_ELEMENTS, board_utils.N_LINES)
    x, y = divmod(position, board_utils.N_LINES)
    return abs(x - correct_x) + abs(y - correct_y)

def advanced_heuristic(node: Node):
    if node.depth >= 2:
        current_distance = manhattan_distance(node.board[node.move], node.move) + \
                           manhattan_distance(node.board[node.parent.move], node.parent.move)

        previous_distance = manhattan_distance(node.parent.board[node.move], node.move) + \
                            manhattan_distance(node.parent.board[node.parent.move], node.parent.move)

        node.weight = node.parent.weight + (current_distance - previous_distance)
    else:
        node.weight = sum([manhattan_distance(node.board[i], i)
                           for i in range(board_utils.N_ELEMENTS)])
    return node.weight

def get_path_from_node(node: Node) -> Queue[tuple[int, int]]:
    path = LifoQueue(node.depth)
    while node.parent is not None:
        path.put(node.move)
        node = node.parent
    return path


def children(node) -> list[Node]:
    moves = board_utils.possible_moves(node.move)
    if node.depth >= 1:
        moves.remove(node.parent.move)
    nodes = [Node(board_utils.move(node.board, move, node.move),
                  node, move, node.depth + 1) for move in moves]
    return nodes
