from ntuple_particle import ntuple_particle as particle
from math import sqrt

class muon(particle):
    def __init__(self,row,i):
        particle.__init__(self,row,i)
        self._mass = 0.1056583715#in GeV

    def energy(self):
        e2 = ( self._row.muPt[self._index]**2 +
               self._row.muPz[self._index]**2 +
               self._mass**2 )        
        return sqrt(e2)

    def pt(self):
        return self._row.muPt[self._index]

    def eta(self):
        return self._row.muEta[self._index]

    def phi(self):
        return self._row.muPhi[self._index]
