from logger import logger, VERBOSE
from queue import Queue, LifoQueue

from src.board import Board

def uniform_cost_search(board: list[list[int]]) -> LifoQueue[tuple[int, int]]:
    """
    Busca de custo uniforme.
    :param board: tabuleiro
    :return: sequencia de movimentos para resolver o tabuleiro enviado
    """
    queue = Queue()
    current: Node = Node(board, None, None, 0, 0)
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
    path = LifoQueue()
    while current.parent is not None:
        path.put(current.move)
        current = current.parent
    return path

def a_star_search(board: Board, advanced=False) -> LifoQueue[tuple[int, int]]:
    heuristic = advanced_heuristic if advanced else basic_heuristic
    return LifoQueue()


def basic_heuristic(board: Board, move: tuple[int]) -> int | float:
    pass

def advanced_heuristic(board: Board, move: tuple[int]) -> int | float:
    pass


def children(node):
    last_move = node.parent.move if node.parent else None
    moves, empty_space = Board.board_state(node.board, last_move)
    nodes = [Node(Board.move(node.board, move, empty_space),
                  node, move, node.depth + 1, 0) for move in moves]
    logger.debug("Found " + str(len(nodes)) + " children at depth " + str(node.depth) + " for parent " + str(node))
    return nodes

class Node:
    def __init__(self, board, parent, move, depth, weight):
        self.board: list[list[int|None]] = board
        self.parent: Node = parent
        self.move: tuple[int] = move
        self.depth = depth
        self.weight = weight
