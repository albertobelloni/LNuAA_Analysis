from ntuple_particle import ntuple_particle as particle

class electron(particle):
    def __init__(self,row,i):
        particle.__init__(self,row,i)
        self._mass = 0.000510998928 #in GeV

    def energy(self):
        return self._row.eleEn[self._index]
    
    def pt(self):
        return self._row.elePt[self._index]
    
    def eta(self):
        return self._row.eleEta[self._index]
    
    def sc_eta(self):
        return self._row.eleSCEta[self._index]
    
    def phi(self):
        return self._row.elePhi[self._index]

    def kTrigMVA(self):
        return self._row.eleIDMVATrig[self._index]

    def missingHits(self):
        return self._row.eleMissHits[self._index]

    def hasMatchedConversion(self):
        return self._row.eleConvVtxFit[self._index]

    def d0(self):
        return self._row.eleD0GV[self._index]

    def dZ(self):
        return self._row.eleDzGV[self._index]

    def sigmaIEtaIEta(self):
        return self._row.eleSigmaIEtaIEta[self._index]

    def dEtaAtVtx(self):
        return self._row.eledEtaAtVtx[self._index]

    def dPhiAtVtx(self):
        return self._row.eledPhiAtVtx[self._index]

    def HoverE(self):
        return self._row.eleHoverE[self._index]

    def trackIsoDR03(self):
        return self._row.eleIsoTrkDR03[self._index]

    def ecalIsoDR03(self):
        barrel = ( abs(self.sc_eta()) < 1.479 )
        return max(0.0, self._row.eleIsoEcalDR03[self._index] - 1*barrel)

    def hcalIsoDR03(self):
        return self._row.eleIsoHcalDR0312[self._index]

    def chargedHadronIsoDR04(self):
        return self._row.elePFChIso04[self._index]

    def neutralHadronIsoDR04(self):
        return self._row.elePFNeuIso04[self._index]

    def photonIsoDR04(self):
        return self._row.elePFPhoIso04[self._index]

    
        
