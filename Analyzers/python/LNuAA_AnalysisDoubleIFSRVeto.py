"""
Specialize LNuAA_BasicSelection to veto events with two i/fsr photons
"""

from LNuAA_PileupReweightedAnalysis import LNuAA_PileupReweightedAnalysis

class LNuAA_AnalysisDoubleIFSRVeto(LNuAA_PileupReweightedAnalysis):
    def __init__(self,tree,outputfile,**kwargs):
        LNuAA_PileupReweightedAnalysis.__init__(self,tree,outputfile,**kwargs)

    def event_veto_mc_photon(self,phos):
        #print 'double photon veto called'
        pho_count = sum( pho.hasIFSRParentage() for pho in phos )
        #if( pho_count >= 2 ):
        #    print 'number of vetoed photons: ',pho_count
        return pho_count >= 2

