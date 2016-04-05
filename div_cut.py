# Implement of div-cut

from tool import Graph
from tool import DivRstSet
import div_astar as astar


def div_cut(graph, k):
    assert(isinstance(graph, Graph.Graph) and isinstance(k, int))
    if not (isinstance(graph, Graph.Graph) and isinstance(k, int)):
        raise TypeError
    if k <= 0:
        raise ValueError
    D = DivRstSet.DivRstSet.new()
    for subG in graph.split():
        subG.compress()
        cutVids = subG.getCutVids()
        if len(cutVids) == 0:
            curD = astar.div_astar(subG, k)
        else:
            # demo
            pass
        D = D.union(curD, k)
    return D


if __name__ == '__main__':
    pass
