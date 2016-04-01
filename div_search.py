# div-search method
# Structure of the parameters
# The origin dataset - tuples = [(id, score), (id, score)..]
# The edgeTable - eTable = ((1, 2, 3), (2))
# The diversity search result - divRet = {1: ((id, score)), 2: ((..))}
# The k-th largest score of any time - kthLrgScore = int

import tool.Graph as grph


def div_search(k, tuples, eTable, div_func):
    assert(k > 0)
    if k >= len(tuples):
        divRet = dict()
        divRet[len(tuples)] = tuple(tuples)
        return divRet
    tuples.sort(key=lambda x: x[1])
    end = 1
    countAddItem = 0
    divRet = {1: tuple(tuples[:end])}
    kthLrgScore = tuples[k - 1][1]
    while maxScore(divRet, len(divRet)) < \
            bestPsbBound(divRet, k, tuples[end][1]):
        end += 1
        countAddItem += 1
        while end == len(tuples) or (countAddItem >= k - max(divRet.keys()) and
                                     kthLrgScore > tuples[end][1]):
            countAddItem = 0
            divRet = div_func(graph=grph.Graph(tuples[:end], eTable), k=k)
    return divRet


def maxScore(divRet, k):
    """return the max value among those sets whose size <= k"""
    assert(isinstance(divRet, dict) and isinstance(k, int))
    ret = 0
    for key, valList in divRet.iteritems():
        if key <= k:
            if not isinstance(valList, tuple):
                raise TypeError
            if key != len(valList):
                raise ValueError
            ret = max(ret, sum([val[1] for val in valList]))
    return ret


def divRetGetScore(divRet, key):
    assert(key in divRet)
    return sum([val[1] for val in divRet[key]])


def bestPsbBound(divRet, k, unseenBound):
    if not (isinstance(divRet, dict) and isinstance(k, int) and
            (isinstance(unseenBound, int) or isinstance(unseenBound, float))):
        raise TypeError
    ret = k * unseenBound
    for key, valList in divRet.iteritems():
        assert(k >= key)
        ret = max(ret, divRetGetScore(divRet, key) + (k - key) * unseenBound)
    return ret


def div_search_cur(**kwarg):
    print kwarg


if __name__ == '__main__':
    testDivRet = {
        1: ((1, 0.5),),
        2: ((1, 0.5), (3, 0.8)),
        3: ((1, 0.5), (2, 0.2), (3, 0.8)),
        4: ((1, 0.5), (2, 0.2), (3, 0.8), (4, 0.1)),
        5: ((3, 0.8), (1, 0.5), (5, 1), (6, 1), (7, 2))
    }
    print maxScore(testDivRet, 5)
    print divRetGetScore(testDivRet, 5)
    print divRetGetScore(testDivRet, 3)
    print divRetGetScore(testDivRet, 2)
    print bestPsbBound(testDivRet, 6, 0.6)
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
    div_search(3, testVertice, eTable, div_search_cur)
