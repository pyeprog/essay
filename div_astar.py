# div-astar implement

from tool import Heap
from div_search import maxScore


def _eGt(e1, e2):
    assert('bound' in e1 and 'bound' in e2)
    return e1['bound'] > e2['bound']


def div_astar(graph, k):
    if not (isinstance(graph, dict) and isinstance(k, int)):
        raise TypeError
    if k < 1:
        raise ValueError
    heap = list()
    divRet = dict()
    initEntry = {'solution': set(), 'pos': -1, 'score': 0, 'bound': 0}
    Heap.HeapPush(heap, initEntry, _eGt)
    graphItems = graph.items().sort(key=lambda x: x[1]['val'])
    for curK in xrange(k, 0, -1):
        astar_search(graph, graphItems, heap, divRet, curK)
        for e in heap:
            e['bound'] = astar_bound(graph, e, curK)
        Heap.Heapify(heap, _eGt)
    return divRet


def astar_search(graph, graphItems, heap, divRet, k):
    if not (isinstance(graphItems, dict) and isinstance(heap, list) and
            isinstance(divRet, dict) and isinstance(k, int)):
        raise TypeError
    while Heap.HeapLen(heap) > 0 and heap[0]['bound'] > maxScore(divRet, k):
        e = Heap.HeapPop(heap, _eGt)
        # graphItems: [(vid, {'nei':set(), 'val':0}),..]
        # e:{'solution': set((vid, score),..),'pos': -1,'score': 0,'bound': 0}
        for i in xrange(e['pos'] + 1, len(graphItems)):
            if len(graphItems[i][1]['nei'].intersection(e['solution'])) == 0:
                enew = {
                    'solution': e['solution'].union(set([graphItems[i][0]])),
                    'pos': i,
                    'score': e['score'] + graphItems[i][1]['val'],
                    'bound': 0}
                enew['bound'] = astar_bound(graphItems, enew, k)
                Heap.HeapPush(heap, enew, _eGt)
                if divRet.get(len(enew['solution']), 0) < enew['score']:
                    retNew = tuple(map(lambda x: (x, graph[x]['val']),
                                       enew['solution']))
                    divRet[len(enew['solution'])] = retNew


def astar_bound(graphItems, e, k):
    bound = e['bound']
    solutionSize = len(e['solution'])
    i = e['pos'] + 1
    while solutionSize < k and i < len(graphItems):
        if len(graphItems[i][1]['nei'].intersection(e['solution'])) == 0:
            bound += graphItems[i][1]['val']
            solutionSize += 1
        i += 1
    return bound


if __name__ == '__main__':
    pass
