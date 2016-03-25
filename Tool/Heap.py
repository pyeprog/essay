# Definition of heap


def HeapPush(heap, item, func):
    if itemCheck(heap, item):
        heap.append(item)
        i = len(heap) - 1
        while ((i - 1) >> 1) >= 0:
            if func(heap[i], heap[(i - 1) >> 1]):
                heap[i], heap[(i - 1) >> 1] = heap[(i - 1) >> 1], heap[i]
                i = ((i - 1) >> 1)
            else:
                break
        return heap


def HeapPop(heap, func):
    assert(HeapLen(heap))
    ret = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    i = 0
    exTrgt = 0
    while (i << 1) + 1 < len(heap):
        exTrgt = i
        if ((i << 1) + 2) < len(heap) and func(heap[(i << 1) + 2], heap[i]):
            exTrgt = ((i << 1) + 2)
        if func(heap[(i << 1) + 1], heap[exTrgt]):
            exTrgt = ((i << 1) + 1)
        if exTrgt != i:
            heap[exTrgt], heap[i] = heap[i], heap[exTrgt]
            i = exTrgt
        else:
            break
    return ret


def HeapLen(heap):
    return len(heap)


def itemCheck(heap, item):
    if HeapLen(heap) > 0 and type(heap[0]) is not type(item):
        return False
    return True


if __name__ == '__main__':
    h = []

    def comp(a, b):
        return a > b

    import random
    for time in xrange(10):
        for i in xrange(random.randint(0, 10230)):
            HeapPush(h, random.random(), comp)
        HeapPush(h, random.random(), comp)
        pre = HeapPop(h, comp)
        while HeapLen(h) > 0:
            post = HeapPop(h, comp)
            if not comp(pre, post):
                print "False"
                break
        print "True"
