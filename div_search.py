# div-search method
# Structure of the parameters
# The origin dataset - tuples = [(id, score), (id, score)..]
# The edgeTable - eTable = ((1, 2, 3), (2))
# The diversity search result - divRet = {1: ((id, score)), 2: ((..))}
# The k-th largest score of any time - kthLrgScore = int

import tool.Graph as graph
import tool.DivRstSet as div


def div_search(k, tuples, eTable, div_func):
    assert(k > 0)
    if k >= len(tuples):
        D = div.DivRstSet(tuples)
        return D
    tuples.sort(key=lambda x: x[1])
    end = 1
    countAddItem = 0
    D = div.DivRstSet(tuples[:end])
    kthLrgScore = tuples[k - 1][1]
    while D.maxScrAll() < D.upbound(k, tuples[end][1]):
        end += 1
        countAddItem += 1
        while end == len(tuples) or (countAddItem >= k - max(D.getKList()) and
                                     kthLrgScore > tuples[end][1]):
            countAddItem = 0
            divRet = div_func(graph=graph.Graph(tuples[:end], eTable), k=k)
    return divRet


if __name__ == '__main__':
    testDivRet = {
        1: ((1, 0.5),),
        2: ((1, 0.5), (3, 0.8)),
        3: ((1, 0.5), (2, 0.2), (3, 0.8)),
        4: ((1, 0.5), (2, 0.2), (3, 0.8), (4, 0.1)),
        5: ((3, 0.8), (1, 0.5), (5, 1), (6, 1), (7, 2))
    }
    testVertice = list()
    import random
    for i in xrange(7):
        testVertice.append((i, random.randint(1, 12)))
    eTable = ((1, 5, 6),
              (0, 2, 5),
              (1, 3, 4),
              (2, 4),
              (2, 3, 5),
              (0, 1, 4, 6, 7),
              (0, 5))
    # div_search(3, testVertice, eTable, div_search_cur)
