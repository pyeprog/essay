# Class method of divRstSet


class DivRstSet(object):
    def __init__(self, iterable, func):
        assert(hasattr(iterable, '__iter__'))
        self._dict = dict()
        for i in iterable:
            k, tuples = func(i, iterable)
            assert(k not in self._dict)
            self._dict[k] = tuples

    def maxScr(self, mink, maxk):
        assert(mink <= maxk)
        assert(isinstance(mink, int) and isinstance(maxk, int))
        maxScore = 0
        for k, tuples in self._dict.iteritems():
            if mink <= k and k <= maxk:
                curSum = sum(map(lambda x: x[1], tuples))
                maxScore = max(maxScore, curSum)
        return maxScore

    def setSet(self, k, tuples):
        assert(isinstance(k, int) and isinstance(tuples, tuple))
        if k != len(tuples):
            raise ValueError
        self._dict[k] = tuples

    def rm(self, k):
        self._dict.pop(k)

    def hasK(self, k):
        return k in self._dict

    def getScr(self, k, *args):
        if self.hasK(k):
            return sum(map(lambda x: x[1], self._dict[k]))
        else:
            assert(len(args))
            assert(isinstance(args[0], (int, float)))
            return args[0]

    def getSet(self, k):
        assert(self.hasK(k))
        return set(map(lambda x: x[0], self._dict[k]))

    def upbound(self, k, usBst):
        if not (isinstance(k, int) and isinstance(usBst, (int, float))):
            raise TypeError
        bstPsbleVal = k * usBst
        for ck in self._dict.iterkeys():
            assert(ck <= k)
            bstPsbleVal = max(bstPsbleVal, self.getScr(ck) + (k - ck) * usBst)
        return bstPsbleVal

    def __getitem__(self, k):
        return self._dict[k]

    def __setitem__(self, k, tuples):
        self.setSet(k, tuples)

    def __str__(self):
        outputStr = ""
        for k, tuples in self._dict.iteritems():
            outputStr += "%s: %s\n" % (k, tuples)
        return outputStr


if __name__ == '__main__':
    testDict = {1: ((1, 3),), 2: ((1, 3), (4, 4)), 3:((1, 3), (4, 4), (5, 1))}

    def proc(i, Dict):
        return i, Dict[i]

    test = DivRstSet(testDict, proc)
    test.setSet(4, ((2, 42), (1, 3), (4, 4), (5, 1)))
    test.rm(4)
    print test.getSet(3)
    print test.getScr(3)
    print test.hasK(5)
    print test.maxScr(1, 3)
    print test.upbound(10, 1)
    test[1] = ((3, 2),)
    print test[1]
