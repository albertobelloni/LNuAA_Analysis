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

    def convSafeElectronVeto(self):
        return self._row.phoEleVeto[self._index]

    def sigmaIEtaIEta(self):
        return self._row.phoSigmaIEtaIEta[self._index]

    def towerHoverE(self):
        return self._row.phoHoverE12[self._index]

    def chargedHadronIsoDR03(self):
        return self._row.phoPFChIso[self._index]

    def neutralHadronIsoDR03(self):
        return self._row.phoPFNeuIso[self._index]

    def photonIsoDR03(self):
        return self._row.phoPFPhoIso[self._index]
