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

    def passesID(self):
        return self._row.elePhi[self._index]
