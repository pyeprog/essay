# div-astar implement

from tool import Graph
from tool import Heap
from tool import HeapE
from tool import DivRstSet
from copy import deepcopy


def _eGt(e1, e2):
    assert(isinstance(e1, HeapE.HeapE) and isinstance(e2, HeapE.HeapE))
    return e2 < e1


def div_astar(graph, k):
    if not (isinstance(graph, Graph.Graph) and isinstance(k, int)):
        raise TypeError
    if k < 1:
        raise ValueError
    heap = list()
    divRslt = DivRstSet.DivRstSet.new()
    e = HeapE.HeapE()
    Heap.HeapPush(heap, e, _eGt)
    for curK in xrange(k, 0, -1):
        astar_search(graph, heap, divRslt, curK)
        for e in heap:
            e.setBnd(astar_bound(graph, e, curK))
        Heap.Heapify(heap, _eGt)
    return divRslt


def astar_search(graph, heap, divRet, k):
    if not (isinstance(graph, Graph.Graph) and isinstance(heap, list) and
            isinstance(divRet, DivRstSet.DivRstSet) and isinstance(k, int)):
        raise TypeError
    while Heap.HeapLen(heap) > 0 and heap[0].getBnd() > divRet.maxScrAll():
        e = Heap.HeapPop(heap, _eGt)
        for i in xrange(e.getPos() + 1, len(graph)):
            if len(graph.getNeiByPos(i).intersection(e.getSol())) == 0:
                newV = graph.getVidByPos(i)
                newVScore = graph.getValByPos(i)
                enew = deepcopy(e).addItmToSol(newV, newVScore, i)
                enew.setBnd(astar_bound(graph, enew, k))
                Heap.HeapPush(heap, enew, _eGt)
                if divRet.getScr(len(enew), 0) < enew.getScr():
                    newTuple = \
                        map(lambda x: (x, graph.getValByV(x)), enew.getSol())
                    divRet.setSet(newTuple)


def astar_bound(graph, e, k):
    bound = e.getBnd()
    solutionSize = len(e)
    i = e.getPos() + 1
    while solutionSize < k and i < len(graph):
        if len(graph.getNeiByPos(i).intersection(e.getSol())) == 0:
            bound += graph.getValByPos(i)
            solutionSize += 1
        i += 1
    return bound


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
    print div_astar(g2, 3)
    print div_astar(g2.compress(), 3)
    anotherList = list()
    anotherList.append((0, 10))
    anotherList.append((1, 8))
    anotherList.append((2, 7))
    anotherList.append((3, 7))
    anotherList.append((4, 6))
    anotherList.append((5, 1))
    anotherList.append((6, 12))
    anotherList.append((7, 13))
    anotherList.append((8, 1))
    anotherList.append((9, 1))
    anotherList.append((10, 1))
    anotherList.append((11, 1))
    anotherList.append((12, 10))
    anotherList.append((13, 9))
    anotherList.append((14, 8))
    anotherList.append((15, 7))
    anotherList.append((16, 6))
    anotherTable = (
        (2, 3, 4),
        (2, 3, 4, 6, 7),
        (0, 1, 5),
        (0, 1, 5, 6, 7, 9),
        (0, 1, 5),
        (2, 3, 4, 9),
        (1, 3, 7, 11, 13, 14),
        (1, 3, 6, 13, 14),
        (9, ),
        (3, 5, 8),
        (11, 12, 13),
        (6, 10),
        (10, 13, 15, 16),
        (6, 7, 10, 12, 14),
        (6, 7, 13, 15, 16),
        (12, 14),
        (12, 14)
    )
    g = Graph.Graph(anotherList, anotherTable)
