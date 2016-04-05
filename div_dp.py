# Implement of method div-dp

from tool import Graph
from tool import DivRstSet
import div_astar as astar


def div_dp(graph, k):
    assert(isinstance(graph, Graph.Graph) and isinstance(k, int))
    if not (isinstance(graph, Graph.Graph) and isinstance(k, int)):
        raise TypeError
    if k <= 0:
        raise ValueError
    D = DivRstSet.DivRstSet.new()
    for subG in graph.split():
        curD = astar.div_astar(subG, k)
        D = D.union(curD, k)
    return D


if __name__ == '__main__':
    testVertice = list()
    testVertice.append((0, 10))
    testVertice.append((1, 8))
    testVertice.append((2, 7))
    testVertice.append((3, 7))
    testVertice.append((4, 6))
    testVertice.append((5, 1))
    eTable = ((2, 3, 4),
              (2, 3, 4),
              (0, 1, 5),
              (0, 1, 5),
              (0, 1, 5),
              (2, 3, 4))
    g = Graph.Graph(testVertice, eTable)
    testVertice2 = list()
    testVertice2.append((0, 10))
    testVertice2.append((1, 9))
    testVertice2.append((2, 8))
    testVertice2.append((3, 7))
    testVertice2.append((4, 6))
    eTable2 = ((1, 3, 4),
               (0, 2),
               (1, 3, 4),
               (0, 2),
               (0, 2))
    g2 = Graph.Graph(testVertice2, eTable2)
    print g
    print div_dp(g, 3)
    print g.compress()
    print div_dp(g.compress(), 3)
