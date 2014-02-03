from ntuple_particle import ntuple_particle as particle
from LNuAA_Analysis.Analyzers.memoized import memoized

from ROOT import TVector3
from math import cosh

_isr = 0x2
_bos = 0xa
_fsr = 0x1a
_np = 0x4

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

    def photonSCRIsoDR04(self):
        return self._row.phoSCRPhoIso04[self._index]

    def photonRandConeIsoDR04(self):
        return self._row.phoRandConePhoIso04[self._index]

    def hasIFSRParentage(self):
        pho_gen_idx = self._row.phoGenIndex[self._index]
        mc_idx = -1
        for idx in xrange(self._row.nMC):
            if( self._row.mcIndex[idx] == pho_gen_idx ):
                mc_idx = idx
                break        
        if( mc_idx == -1 ):
            return False;
        # if it's not non-prompt and it's isr/from a boson/fsr
        # then we should call it ifsr/boson
        return ( ( self._row.mcParentage[mc_idx] & _np ) != _np and
                 ( self._row.mcParentage[mc_idx] & _isr == _isr or
                   self._row.mcParentage[mc_idx] & _bos == _bos or
                   self._row.mcParentage[mc_idx] & _fsr == _fsr   ) )
