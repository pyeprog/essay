# Class method of divRstSet


class DivRstSet(object):
    def __init__(self, iterable, func):
        assert(hasattr(iterable, '__iter__'))
        self._dict = dict()
        self._scoreDict = dict()
        for k, tuples in func(iterable):
            assert(k not in self._dict)
            self._dict[k] = tuples
            self._scoreDict[k] = sum(map(lambda x: x[1], tuples))

    @classmethod
    def new(cls, *args):
        divSet = DivRstSet({}, DivRstSet._dictTrans)
        for each in args:
            divSet.setSet(each)
        return divSet

    @classmethod
    def _dictTrans(cls, dictionary):
        assert(isinstance(dictionary, dict))
        return dictionary.iteritems()

    @classmethod
    def _tuplesTrans(cls, tuples):
        assert(isinstance(tuples, (list, tuple, set)))
        return tuple([(len(tuples), tuple(tuples))])

    def maxScr(self, mink, maxk):
        assert(mink <= maxk)
        assert(isinstance(mink, int) and isinstance(maxk, int))
        maxScore = 0
        for k, tuples in self._dict.iteritems():
            if mink <= k and k <= maxk:
                curSum = sum(map(lambda x: x[1], tuples))
                maxScore = max(maxScore, curSum)
        return maxScore

    def maxScrAll(self):
        kList = self._dict.keys()
        maxScrV = 0
        if len(kList):
            maxScrV = self.maxScr(min(kList), max(kList))
        return maxScrV

    def setSet(self, iterable):
        if isinstance(iterable, (list, tuple, set)):
            self._dict[len(iterable)] = tuple(iterable)
            self._scoreDict[len(iterable)] = sum(map(lambda x: x[1], iterable))
        elif isinstance(iterable, dict):
            for k, t in iterable.iteritems():
                self[k] = t
        return self

    def rm(self, k):
        self._dict.pop(k)

    def hasK(self, k):
        return k in self._dict and k in self._scoreDict

    def getScr(self, k, *args):
        if self.hasK(k):
            return self._scoreDict[k]
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

    def getKList(self):
        return self._dict.keys()

    def __getitem__(self, k):
        return self._dict[k]

    def __setitem__(self, k, tuples):
        assert(k == len(tuples))
        self.setSet(tuples)

    def __str__(self):
        outputStr = ""
        for k, tuples in self._dict.iteritems():
            outputStr += "%s: %s\n" % (k, tuples)
        return outputStr

    def __eq__(self, other):
        assert(isinstance(other, DivRstSet))
        isEqual = True
        for k in self.getKList():
            if other.hasK(k):
                isEqual &= (self[k] == other[k])
                if not isEqual:
                    return False
            else:
                return False
        return isEqual

    def union(self, other, k):
        assert(isinstance(other, DivRstSet) and isinstance(k, int))
        unionedSet = DivRstSet.new()
        for i in xrange(1, k + 1):
            for j in xrange(0, i + 1):
                if (other.hasK(j) or j == 0) and (self.hasK(i - j) or i == j):
                    scoreSum = other.getScr(j, 0) + self.getScr(i - j, 0)
                    if scoreSum > unionedSet.getScr(i, 0):
                        newSet = tuple()
                        if other.hasK(j):
                            newSet += other[j]
                        if self.hasK(i - j):
                            newSet += self[i - j]
                        unionedSet.setSet(newSet)
        return unionedSet

    def compete(self, other, k):
        assert(isinstance(other, DivRstSet) and isinstance(k, int))
        competeSet = DivRstSet.new()
        for i in xrange(1, k + 1):
            if self.getScr(i, 0) > other.getScr(i, 0):
                competeSet.setSet(self[i])
            elif self.getScr(i, 0) < other.getScr(i, 0):
                competeSet.setSet(other[i])
            elif self.getScr(i, 0) != 0:
                competeSet.setSet(self[i])
        return competeSet


if __name__ == '__main__':
    testDict = {1: ((1, 3),), 2: ((1, 3), (4, 4)), 3: ((1, 3), (4, 4), (5, 1))}
    test = DivRstSet(testDict, DivRstSet._dictTrans)
    test.setSet(((2, 42), (1, 3), (4, 4), (5, 1)))
    test.rm(4)
    print test.getScr(1)
    print test.getScr(2)
    print test.getScr(3)
    print test.hasK(5)
    print test.maxScr(1, 3)
    print test.maxScrAll()
    print test.upbound(10, 1)
    test[1] = ((3, 2),)
    print test[1]
    testTuples = [(1, 3), (2, 4), (3, 53)]
    testTuples1 = set([(1, 3), (2, 4), (3, 53)])
    testTuples2 = ((1, 3), (2, 4), (3, 53))
    print DivRstSet(testTuples, DivRstSet._tuplesTrans)
    print DivRstSet(testTuples1, DivRstSet._tuplesTrans)
    print DivRstSet(testTuples2, DivRstSet._tuplesTrans)
    test1 = DivRstSet.new(testDict)
    test = DivRstSet.new(testDict, testTuples1)
    print 'equal', test1 == test
    print "test", test.getScr(3)
    print test
    print test.getKList()
    t1 = DivRstSet.new(testDict)
    t2 = DivRstSet.new(testTuples)
    print t1.union(t2, 3)
    d1 = {1: ((1, 10), ),
          2: ((1, 10), (2, 8)),
          3: ((3, 7), (4, 7), (5, 6))}
    d2 = {1: ((11, 10),),
          2: ((11, 10), (13, 8)),
          3: ((12, 9), (14, 7), (15, 6))}
    s1 = DivRstSet.new(d1)
    s2 = DivRstSet.new(d2)
    print s1.compete(s2, 5)
    print s1.union(DivRstSet.new(), 5)
    print s1.compete(DivRstSet.new(), 5)
    print DivRstSet.new().union(s2, 5)
    print DivRstSet.new().compete(s2, 5)
