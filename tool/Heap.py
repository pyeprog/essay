# Definition of heap


def HeapifyFromTop(heap, func):
    assert(isinstance(heap, list))
    if HeapLen(heap) > 1:
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


def HeapifyFromBtm(heap, heapLen, func):
    assert(isinstance(heap, list))
    assert(heapLen <= len(heap))
    if HeapLen(heap) > 1:
        i = heapLen - 1
        while ((i - 1) >> 1) >= 0:
            if func(heap[i], heap[(i - 1) >> 1]):
                heap[i], heap[(i - 1) >> 1] = heap[(i - 1) >> 1], heap[i]
                i = ((i - 1) >> 1)
            else:
                break


def Heapify(heap, func):
    assert(isinstance(heap, list))
    if HeapLen(heap) > 1:
        for i in xrange(2, HeapLen(heap) + 1):
            HeapifyFromBtm(heap, i, func)
    return heap


def HeapPush(heap, item, func):
    assert(isinstance(heap, list))
    if _itemCheck(heap, item):
        heap.append(item)
        HeapifyFromBtm(heap, len(heap), func)
        return heap


def HeapPop(heap, func):
    assert(isinstance(heap, list))
    assert(HeapLen(heap))
    ret = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    HeapifyFromTop(heap, func)
    return ret


def HeapReplace(heap, item, func):
    assert(isinstance(heap, list))
    assert(HeapLen(heap) > 0)
    heap[0] = item
    HeapifyFromTop(heap, func)


def HeapLen(heap):
    assert(isinstance(heap, list))
    return len(heap)


def _itemCheck(heap, item):
    assert(isinstance(heap, list))
    if HeapLen(heap) > 0 and type(heap[0]) is not type(item):
        return False
    return True


if __name__ == '__main__':
    h = []

    def comp(a, b):
        return a < b

    import random
    for i in xrange(10):
        testList = []
        for i in xrange(100):
            testList.append(random.randint(-100, 100))
        Heapify(testList, comp)
        pre = -100
        while HeapLen(testList):
            cur = HeapPop(testList, comp)
            assert(pre <= cur)
            pre = cur
        print True
