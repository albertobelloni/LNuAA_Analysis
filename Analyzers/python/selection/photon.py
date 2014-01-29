from ntuple_particle import ntuple_particle as particle

from ROOT import TVector3
from math import cosh

_ifsr_parent_mask = 0x12
_nonprompt_mask   = 0x4

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

    def hasIFSRParentage(self):
        mc_idx = -1
        for idx in xrange(self._row.nMC):
            if( self._row.mcIndex[idx] == self._row.phoGenIndex[self._index] ):
                mc_idx = idx
                break        
        if( mc_idx == -1 ):
            return False;         
        return ( ( self._row.mcParentage[mc_idx] & _ifsr_parent_mask ) != 0 and
                 ( self._row.mcParentage[mc_idx] & _nonprompt_mask )   != 0x4 )
