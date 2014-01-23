from ntuple_particle import ntuple_particle as particle

from ROOT import TVector3
from math import cosh

class photon(particle):
    def __init__(self,row,i):
        particle.__init__(self,row,i)
        self._mass = 0.0 #in GeV        

    def energy(self):
        return self._row.phoSCE[self._index]

    def pt(self):
        return self._row.phoSCE[self._index]/cosh(self.eta())

    def eta(self):
        return self._row.phoEta[self._index]

    def sc_eta(self):
        return self._row.phoSCEta[self._index]

    def phi(self):
        return self._row.phoPhi[self._index]
