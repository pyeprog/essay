# class method of heap entry

import copy


class HeapE(object):
    def __init__(self, Dict=None):
        self._dict = dict()
        self._dict['sol'] = set()
        self._dict['pos'] = -1
        self._dict['scr'] = 0
        self._dict['bnd'] = 0
        if isinstance(Dict, dict):
            for key in self._dict.iterkeys():
                assert(key in Dict)
                assert(isinstance(self._dict[key], type(Dict[key])))
                self._dict[key] = Dict[key]

    def addItmToSol(self, item, score, *args):
        if not (isinstance(item, int) and isinstance(score, (int, float))):
            raise TypeError
        self._dict['sol'].add(item)
        self._dict['scr'] += score
        if len(args) and isinstance(args[0], int):
            self._dict['pos'] = args[0]
        return self

    def getSol(self):
        return self._dict['sol']

    def setSol(self, sol, scr):
        if not (isinstance(sol, set) and isinstance(scr, (float, int))):
            raise TypeError
        self._dict['sol'] = sol
        self._dict['scr'] = scr
        return self

    def getPos(self):
        return self._dict['pos']

    def setPos(self, pos):
        assert(isinstance(pos, int))
        self._dict[pos] = pos
        return self

    def getScr(self):
        return self._dict['scr']

    def getBnd(self):
        return self._dict['bnd']

    def setBnd(self, bnd):
        assert(isinstance(bnd, (int, float)))
        self._dict['bnd'] = bnd
        return self

    def toDict(self):
        return copy.deepcopy(self._dict)

    def __lt__(self, other):
        assert(isinstance(other, HeapE))
        return self._dict['bnd'] < other._dict['bnd']

    def __str__(self):
        outputStr = ""
        for key, value in self._dict.iteritems():
            outputStr += "%s: %s\n" % (key, value)
        return outputStr

    def __deepcopy__(self, memodict={}):
        return HeapE(self.toDict())

if __name__ == '__main__':
    A = HeapE()
    B = copy.deepcopy(A)
    B.addItmToSol(1, 23).addItmToSol(2, 12, 2).setBnd(3)
    print B
    print A
    print A < B
