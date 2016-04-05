# Use class to implement graph
# _dict = {
#   vertexId : {nei = set(), val = someVal}
# }


class Graph(object):
    def __init__(self, tuples, eTable):
        if not (hasattr(tuples, '__iter__') and hasattr(eTable, '__iter__')):
            raise TypeError
        self._dict = dict()
        for vid, score in tuples:
            assert(vid not in self._dict)
            self._dict[vid] = dict()
            self._dict[vid]['val'] = score
            self._dict[vid]['nei'] = set(eTable[vid])
        self.sort()

    def _setDict(self, otherD):
        if not isinstance(otherD, dict):
            raise TypeError
        self._dict = otherD

    def addV(self, vid, score):
        assert(vid not in self._dict)
        self._dict[vid] = dict()
        self._dict[vid]['val'] = score
        self._dict[vid]['nei'] = set()
        self.sort()
        return self

    def addE(self, vid1, vid2, *args):
        assert(vid1 in self._dict and vid2 in self._dict)
        assert(vid2 not in self._dict[vid1]['nei'])
        assert(vid1 not in self._dict[vid2]['nei'])
        self._dict[vid1]['nei'].add(vid2)
        self._dict[vid2]['nei'].add(vid1)

    def delV(self, vid, *args):
        assert(vid in self._dict)
        vDict = self._dict.pop(vid)
        for neiVid in vDict['nei']:
            self._dict[neiVid]['nei'].remove(vid)
        self.sort()
        return vDict

    def delE(self, vid1, vid2, *args):
        assert(vid1 in self._dict and vid2 in self._dict)
        self._dict[vid1]['nei'].remove(vid2)
        self._dict[vid2]['nei'].remove(vid1)

    def subG(self, vertice):
        if not hasattr(vertice, '__iter__'):
            raise TypeError
        newG = Graph([], [])
        newD = dict()
        newVSet = set(vertice)
        for vid in vertice:
            assert(vid not in newD and self.hasV(vid))
            newD[vid] = dict()
            newD[vid]['val'] = self.getValByV(vid)
            newD[vid]['nei'] = self.getNeiByV(vid) & newVSet
        newG._setDict(newD)
        newG.sort()
        return newG

    def split(self, *args):
        subGList = list()
        leftVids = self.getVids()
        while len(leftVids):
            curVList = list()
            stack = list()
            stack.append(leftVids.pop())
            while len(stack):
                curV = stack.pop()
                curVList.append(curV)
                for neiV in self.getNeiByV(curV):
                    if neiV in leftVids:
                        leftVids.remove(neiV)
                        stack.append(neiV)
            subGList.append(self.subG(curVList))
        return subGList

    def compress(self):
        delVids = set()
        processedVids = set()
        for vid, Dict in self._items:
            if vid not in delVids:
                processedVids.add(vid)
                vConductG = self.getNeiByV(vid).union(set([vid]))
                for neiVid in (Dict['nei'] - processedVids - delVids):
                    neiVConductG = self.getNeiByV(neiVid).union(set([neiVid]))
                    if vConductG.issubset(neiVConductG):
                        delVids.add(neiVid)
        for vid in delVids:
            self.delV(vid)
        self.sort()
        return self

    def getVids(self):
        return set(self._dict.keys())

    def getPosByV(self, vid):
        return self._items.index((vid, self._dict[vid]))

    def getVidByPos(self, pos):
        return self._items[pos][0]

    def getValByV(self, vid):
        assert(vid in self._dict)
        return self._dict[vid]['val']

    def getNeiByV(self, vid):
        assert(vid in self._dict)
        return self._dict[vid]['nei']

    def getValByPos(self, pos):
        assert(isinstance(pos, int) and pos >= 0)
        return self._items[pos][1]['val']

    def getNeiByPos(self, pos):
        assert(isinstance(pos, int) and pos >= 0)
        return self._items[pos][1]['nei']

    def hasV(self, vid):
        return vid in self._dict

    def hasE(self, vid1, vid2):
        return (vid1 in self._dict and vid2 in self._dict and
                vid1 in self._dict[vid2]['nei'] and
                vid2 in self._dict[vid1]['nei'])

    def getCutVids(self):
        parent = dict().fromkeys(self._dict, -1)
        isCutVids = dict().fromkeys(self._dict, 0)
        processed = dict().fromkeys(self._dict, 0)
        discTime = dict().fromkeys(self._dict, -1)
        minDTime = dict().fromkeys(self._dict, 0)

        def _ap(vid):
            # problematic
            assert(self.hasV(vid) and isinstance(_ap.time, int))
            children = 0
            processed[vid] = 1
            discTime[vid] = _ap.time
            minDTime[vid] = _ap.time
            _ap.time += 1
            for neiVid in self.getNeiByV(vid):
                if not processed[neiVid]:
                    children += 1
                    parent[neiVid] = vid
                    _ap(neiVid)
                    minDTime[vid] = min(minDTime[neiVid], minDTime[vid])
                    if parent[vid] == -1 and children > 1:
                        isCutVids[vid] = 1
                    if parent[vid] != -1 and discTime[vid] <= minDTime[neiVid]:
                        isCutVids[vid] = 1
                elif neiVid != parent[vid]:
                    minDTime[vid] = min(discTime[neiVid], minDTime[vid])

        vidSet = self.getVids()
        _ap.time = 0
        for vid in vidSet:
            if not processed[vid]:
                _ap(vid)
        return set([vid for vid, val in isCutVids.iteritems() if val])

    def __contains__(self, vid):
        return self.hasV(vid)

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, pos):
        return self._items[pos]

    def sort(self, reverse=True):
        self._items = self._dict.items()
        self._items.sort(key=lambda x: x[1]['val'], reverse=reverse)

    def __str__(self):
        outputStr = ""
        for vid, val in self._dict.iteritems():
            outputStr += "%s: val->%s nei->%s\n" % (vid, val['val'], val['nei'])
        return outputStr

    def __deepcopy__(self, memodict={}):
        return self.subG(self.getVids())

    def __eq__(self, other):
        assert(isinstance(other, Graph))
        isEqual = True
        for vid in self.getVids():
            if other.hasV(vid):
                isEqual &= self.getValByV(vid) == other.getValByV(vid)
                isEqual &= self.getNeiByV(vid) == other.getNeiByV(vid)
                if not isEqual:
                    return False
            else:
                return False
        return isEqual


if __name__ == '__main__':
    import random
    testVertice = list()
    for i in xrange(8):
        testVertice.append((i, random.randint(0, 100)))
    eTable = ((1, 5, 6),
              (0, 2, 5),
              (1, 3, 4),
              (2, 4),
              (2, 3, 5),
              (0, 1, 4, 6, 7),
              (0, 5),
              (5,))
    g = Graph(testVertice, eTable)
    print len(g.split())
    subg = g.subG([0, 1, 5])
    for i in xrange(len(g)):
        print g[i]
    print subg.getNeiByV(5)
    print g
    print 'compress'
    print g.compress()
    testVertice = list()
    for i in xrange(10):
        testVertice.append((i, random.randint(0, 100)))
    eTable = (tuple(), tuple(), tuple(), tuple(), tuple(), tuple(), tuple(),
              tuple([8]), (9, 7), tuple([8]))
    g = Graph(testVertice, eTable)
    print len(g.split())
    for ig in g.split():
        print ig
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
    g = Graph(anotherList, anotherTable)
    import copy
    gc = copy.deepcopy(g)
    print g
    print g.compress()
    print 'compress', g.getCutVids()
    print 'uncompress', gc.getCutVids()
    t1List = list()
    t1List.append((0, 1))
    t1List.append((1, 1))
    t1List.append((2, 1))
    t1List.append((3, 1))
    t1List.append((4, 1))
    t1T = ((1, 2, 3),
           (0, 2),
           (0, 1),
           (0, 4),
           (3,))
    gt = Graph(t1List, t1T)
    print gt.getCutVids()
    t2List = list()
    t2List.append((0, 1))
    t2List.append((1, 1))
    t2List.append((2, 1))
    t2List.append((3, 1))
    t2List.append((4, 1))
    t2List.append((5, 1))
    t2List.append((6, 1))
    t2T = ((1, 2),
           (0, 2, 3, 4, 6),
           (0, 1),
           (1, 5),
           (1, 5),
           (3, 4),
           (1, ))
    gt2 = Graph(t2List, t2T)
    print gt2.getCutVids()
    t3List = list()
    t3List.append((0, 1))
    t3List.append((1, 1))
    t3List.append((2, 1))
    t3List.append((3, 1))
    t3T = ((1, ),
           (0, 2),
           (1, 3),
           (2, ))
    gt3 = Graph(t3List, t3T)
    print gt3.getCutVids()
