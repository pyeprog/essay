# The tuple of input has the structure of (id, score)

import tool.Heap as Heap


def _lt(tupleA, tupleB):
    if not (isinstance(tupleA, tuple) and isinstance(tupleB, tuple)):
        raise TypeError
    return tupleA[1] < tupleB[1]


def _gt(tupleA, tupleB):
    if not (isinstance(tupleA, tuple) and isinstance(tupleB, tuple)):
        raise TypeError
    return tupleA[1] > tupleB[1]


def topk(tuples, k, func):
    ret = []
    incremental(tuples, 0, ret, k, func)
    return ret


def incremental(tuples, startIndex, ret, expectedSize, func):
    if not (isinstance(tuples, list) and isinstance(ret, list) and
            isinstance(startIndex, int) and isinstance(expectedSize, int)):
        raise TypeError
    if not (0 <= startIndex and startIndex < len(tuples)):
        raise IndexError
    if len(ret) >= expectedSize:
        return ret
    if len(tuples) - startIndex < expectedSize:
        return ret+tuples[startIndex:]
    while len(ret) < expectedSize:
        Heap.HeapPush(ret, tuples[startIndex], func)
        startIndex += 1
    for i in xrange(startIndex, len(tuples)):
        if tuples[i][1] > ret[0][1]:
            tuples[i], ret[0] = ret[0], tuples[i]
            Heap.HeapifyFromTop(ret, func)
    return ret


if __name__ == '__main__':
    import random

    def randomTupleGen(k):
        for i in xrange(k):
            yield (i, random.random())

    for c in xrange(100):
        tuples = []
        k = random.randint(0, 12312)
        gen = randomTupleGen(k)
        for i in gen:
            tuples.append(i)
        orTuples = tuples[:]
        ret = topk(tuples, 1, _lt)
        if len(ret) < len(tuples):
            incremental(tuples, len(ret), ret, 999, _lt)
        orTuples.sort(key=lambda x: x[1], reverse=True)
        for e in ret:
            assert(orTuples.index(e) < k)
        print True
