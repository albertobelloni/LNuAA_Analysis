from ntuple_particle import ntuple_particle as particle
from math import sqrt
from LNuAA_Analysis.Analyzers.memoize import memoized

pfmu_mask  = 1<<5
gblmu_mask = 1<<1

class muon(particle):
    def __init__(self,row,i):
        particle.__init__(self,row,i)
        self._mass = 0.1056583715#in GeV

    @memoized
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

    def isGlobalMuon(self):
        return ( self._row.muType[self._index] & gblmu_mask == gblmu_mask)

    def isPFMuon(self):
        return ( self._row.muType[self._index] & pfmu_mask  == pfmu_mask )

    def globalChi2(self):
        return self._row.muChi2NDF[self._index]

    def trackerOnlyChi2(self):
        return self._row.muInnerChi2NDF[self._index]

    def nValidMuonHits(self):
        return self._row.muNumberOfValidMuonHits[self._index]

    def nValidPixelHits(self):
        return self._row.muNumberOfValidPixelHits[self._index]

    def nLayersWithMeasurement(self):
        return self._row.muNumberOfValidTrkLayers[self._index]

    def nMatchedStations(self):
        return self._row.muStations[self._index]

    def d0(self):
        return self._row.muD0GV[self._index]

    def dZ(self):
        return self._row.muDzGV[self._index]

    def chargedHadronIsoDR04(self):
        return self._row.muPFIsoR04_CH[self._index]

    def neutralHadronIsoDR04(self):
        return self._row.muPFIsoR04_NH[self._index]

    def photonIsoDR04(self):
        return self._row.muPFIsoR04_Pho[self._index]

    def puIsoDR04(self):
        return self._row.muPFIsoR04_PU[self._index]
