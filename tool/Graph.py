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

    def _setDict(self, otherD):
        if not isinstance(otherD, dict):
            raise TypeError
        self._dict = otherD

    def addV(self, vid, score):
        assert(vid not in self._dict)
        self._dict[vid] = dict()
        self._dict[vid]['val'] = score
        self._dict[vid]['nei'] = set()
        return self

    def addE(self, vid1, vid2, *args):
        assert(vid1 in self._dict and vid2 in self._dict)
        assert(vid2 not in self._dict[vid1]['nei'])
        assert(vid1 not in self._dict[vid2]['nei'])
        self._dict[vid1]['nei'].add(vid2)
        self._dict[vid2]['nei'].add(vid1)

    def delV(self, vid, *args):
        assert(vid in self._dict)
        return self._dict.pop(vid)

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
            newD[vid]['val'] = self.getVVal(vid)
            newD[vid]['nei'] = self.getNei(vid) & newVSet
        newG._setDict(newD)
        return newG

    def getVVal(self, vid):
        assert(vid in self._dict)
        return self._dict[vid]['val']

    def getNei(self, vid):
        assert(vid in self._dict)
        return self._dict[vid]['nei']

    def hasV(self, vid):
        return vid in self._dict

    def hasE(self, vid1, vid2):
        return (vid1 in self._dict and vid2 in self._dict and
                vid1 in self._dict[vid2]['nei'] and
                vid2 in self._dict[vid1]['nei'])

    def __contains__(self, vid):
        return self.hasV(vid)

    def __len__(self):
        return len(self._dict)

    def __getitem__(self, vid):
        assert(vid < len(self._dict))
        try:
            return self.items[vid]
        except AttributeError:
            self.updtG()
            return self.items[vid]

    def updtG(self, reverse=True):
        self.items = self._dict.items()
        self.items.sort(key=lambda x: x[1]['val'], reverse=reverse)

    def __str__(self):
        outputStr = ""
        for vid, val in self._dict.iteritems():
            outputStr += "%s: val->%s nei->%s\n" % (vid, val['val'], val['nei'])
        return outputStr


if __name__ == '__main__':
    import random
    testVertice = list()
    for i in xrange(7):
        testVertice.append((i, random.randint(0, 100)))
    eTable = ((1, 5, 6),
              (0, 2, 5),
              (1, 3, 4),
              (2, 4),
              (2, 3, 5),
              (0, 1, 4, 6, 7),
              (0, 5))
    g = Graph(testVertice, eTable)
    subg = g.subG([0, 1, 5])
    for i in xrange(len(g)):
        print g[i]
    print subg.getNei(5)
