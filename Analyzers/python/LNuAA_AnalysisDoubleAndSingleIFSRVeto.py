"""
Specialize LNuAA_BasicSelection to veto events with one i/fsr photons
"""

from LNuAA_BasicSelectionAnalysis import LNuAA_BasicSelectionAnalysis

class LNuAA_AnalysisDoubleIFSRVeto(LNuAA_BasicSelectionAnalysis):
    def __init__(self,tree,outputfile,**kwargs):
        LNuAA_BasicSelectionAnalysis.__init__(self,tree,outputfile,**kwargs)

    def event_veto_mc_photon(self,phos):
        print 'single photon veto called'
        pho_count = sum( pho.hasIFSRParentage() for pho in phos )
        print 'number of vetoed photons: ',pho_count
        return pho_count >= 1

