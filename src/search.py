from logger import logger, VERBOSE
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


def uniform_cost_search(board: list[list[int]]) -> Queue[tuple[int, int]]:
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
            if board_str in visited:
                continue
            else:
                visited.add(board_str)
            queue.put(item)
        current = queue.get()

    logger.log(VERBOSE, "Visited: " + str(total_visited) + " nodes")
    return get_path_from_node(current)


def a_star_search(board: list[list[int]], advanced=False) -> Queue[tuple[int, int]]:
    heuristic = advanced_heuristic if advanced else basic_heuristic
    queue = PriorityQueue()
    current = Node(board, None, None, 0)
    visited = set()
    total_visited = 0
    while not Board.game_is_over(current.board):
        total_visited += 1
        for item in children(current):
            board_str = "".join(["".join([str(i) for i in line]) for line in item.board])
            if board_str in visited:
                continue
            else:
                visited.add(board_str)
            item.weight = current.weight + heuristic(item)
            queue.put(item)
        current = queue.get()

    logger.log(VERBOSE, "Visited: " + str(total_visited) + " nodes")
    return get_path_from_node(current)


def basic_heuristic(node: Node):
    flat_board = Board.flatten(node.board)
    score = len(Board.GOAL)
    for i in range(len(flat_board)):
        score -= Board.GOAL[i] == flat_board[i]
    return score * HEURISTIC_WEIGHT


def advanced_heuristic(node: Node):
    return 0


def get_path_from_node(node: Node) -> Queue[tuple[int, int]]:
    path = LifoQueue()
    while node.parent is not None:
        path.put(node.move)
        node = node.parent
    logger.log(VERBOSE, "Number of moves: " + str(path.qsize()))
    return path


def children(node) -> list[Node]:
    last_move = node.parent.move if node.parent else None
    moves, empty_space = Board.board_state(node.board, last_move)
    nodes = [Node(Board.move(node.board, move, empty_space),
                  node, move, node.depth + 1) for move in moves]
    logger.debug("Found " + str(len(nodes)) + " children at depth " + str(node.depth) + " for parent " + str(node))
    return nodes
