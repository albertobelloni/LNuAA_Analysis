"""
analysis with pileup reweighting
"""

# import the Base analysis class
from LNuAA_BasicSelectionAnalysis import LNuAA_BasicSelectionAnalysis
import ROOT

# define our analyzer class - it must be called MyAnalyzer, since that is
# the name of this file.  It inherits from MegaBase.
class LNuAA_PileupReweightedAnalysis(LNuAA_BasicSelectionAnalysis):
    # We have to define the path that the target ntuple can be found.
    tree = 'ggNtuplizer/EventTree'

    def __init__(self, tree, outputfile, **kwargs):
        LNuAA_BasicSelectionAnalysis.__init__(self,tree,outputfile,**kwargs)
        """
        The __init__ method must take the following arguments:

        tree:       a ROOT TTree that will be processed.
        outputfile: a ROOT TFile (already open) to write output into
        **kwargs:   optionally extra keyword args can be passed (advanced)
        """
        #### get pileup histogram for this file!
        # this is really hacky but it works 
        pupath = str(self.tree.GetDirectory().GetPath()).split('Job_')[0]
        pupath += 'histograms.root'
        pwd = ROOT.gDirectory.GetPath()
        mcpufile = ROOT.TFile.Open(pupath)
        ROOT.gDirectory.cd(pwd)
        self.mc_pileup_histo = mcpufile.Get('ggNtuplizer').Get('hPUTrue')\
                               .Clone('mcpuhisto')
        self.mc_pileup_histo.SetDirectory(0)
        self.mc_pileup_histo.Scale(1./self.mc_pileup_histo.Integral())
        mcpufile.Close()
        datapufile = ROOT.TFile.Open('root://eoscms.cern.ch//store/user/lgray/pileup_distributions/run2012ABCD_pileup_true.root')
        ROOT.gDirectory.cd(pwd)
        self.pileup_weights = datapufile.Get('pileup').Clone('datapuhisto')
        self.pileup_weights.SetDirectory(0)
        self.pileup_weights.Scale(1./self.pileup_weights.Integral())
        datapufile.Close()
        self.pileup_weights.Divide(self.mc_pileup_histo)
    
    def calc_puweight(self,row):
        thebin = self.pileup_weights.FindBin(row.puTrue[0])
        return self.pileup_weights.GetBinContent(thebin)

    
