import tool.Heap as Heap


def _lt(tupleA, tupleB):
    if type(tupleA) is not tuple or type(tupleB) is not tuple:
        raise TypeError
    return tupleA[1] < tupleB[1]


def topk(tuples, k):
    if type(tuples) is not list or type(k) is not int:
        raise TypeError
    if len(tuples) <= k:
        return tuples
    ret = list()
    for i in xrange(k):
        Heap.HeapPush(ret, tuples[i], _lt)
    for i in xrange(k, len(tuples)):
        if tuples[i][1] > ret[0][1]:
            Heap.HeapReplace(ret, tuples[i], _lt)
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
        ret = topk(tuples, 999)
        tuples.sort(key=lambda x: x[1], reverse=True)
        for e in ret:
            assert(tuples.index(e) < k)
        print True
