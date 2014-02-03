#represents a particle that's built from a particular sub-row
#in a non-flat ntuple (like ggNtuple)

import ROOT
from ROOT import TLorentzVector

class ntuple_particle(object):
    def __init__(self,row,i):
        self._row = row
        self._index = i
        self._mass = 0

    def __repr__(self):
        print "%s%s%s"%(self._row,self._index,self._mass)

    def energy(self):
        pass
    def pt(self):
        pass
    def eta(self):
        pass
    def phi(self):
        pass
    
    def p4(self):
        thep4 = TLorentzVector()
        thep4.SetPtEtaPhiE(self.pt(),self.eta(),self.phi(),self.energy())
        return thep4

    def passesID():
        pass
    
