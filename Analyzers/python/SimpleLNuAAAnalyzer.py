'''

Example Ntuple Analyzer
=======================

A simple analyzer to make histograms using the "mega" script.
This analyzes Zmumu events.

An analyzer script has three main requirements:

 1. there is a class with the same name as the file
 2. that class inherits from the MegaBase class
 3. the class has the following methods
    * __init__(self, tree, outputfile, **kwargs)
    * begin(self) - initializing/booking histograms
    * process(self) - loop over the tree and fill the histograms
    * finish(self) - cleanup (optional)
    * the class must define the 'path/to/the/Ntuple' as the class variable
      'tree'

Author: Evan K. Friis, UW Madison

'''

import heapq
# import the MegaBase class
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

# Import various other code used by this module
# We need this because of the "type = ROOT.TH2F" below
import ROOT


# define our analyzer class - it must be called MyAnalyzer, since that is
# the name of this file.  It inherits from MegaBase.
class SimpleLNuAAAnalyzer(MegaBase):
    # We have to define the path that the target ntuple can be found.
    tree = 'ggNtuplizer/EventTree'

    def __init__(self, tree, outputfile, **kwargs):
        MegaBase.__init__(self,tree,outputfile,**kwargs)
        '''
        The __init__ method must take the following arguments:

        tree:       a ROOT TTree that will be processed.
        outputfile: a ROOT TFile (already open) to write output into
        **kwargs:   optionally extra keyword args can be passed (advanced)
        '''
        self.tree = tree  # need to keep a reference to this for later
        self.outputfile = outputfile
        

    def begin(self):
        ''' Let's book some histograms.

        Let's pretend we have two regions in our analysis,
        "signal" and "sideband."  We'll organize our histograms into
        directories accordingly.

        The histograms are available via a dictionary called "histograms".

        The keys of the dictionary are the full paths to the histograms.

        '''

        # MegaBase includes some convenience methods for booking histograms.
        # This books a 200 bin TH1F called "MyHistoName" into the "signal"
        # folder.
        self.book('signal', 'muon_pT', 'p_{T}', 200, 10, 110)
        self.book('signal', 'electron_pT', 'p_{T}', 200, 10, 110)
        self.book('signal', 'photon1_pT', 'p_{T}', 200, 10, 110)
        self.book('signal', 'photon2_pT', 'p_{T}', 200, 10, 110)

        # How to make a 2D histo
        #self.book('signal', 'PtVsEta', 'p_{T} vs. #eta',
        #          200, 0, 100, 100, -2.5, 2.5, type=ROOT.TH2F)

        # In our sideband
        #self.book('sideband', 'MyPtHistoName', 'p_{T}', 200, 0, 100)

    def process(self):
        ''' Our analysis logic. '''
        # Loop over the tree
        for row in self.tree:
            if row.nPho == 0:
                continue
            #require certain objects be in our event
            if row.nMu != 0:
                maxMuon_pt = max(row.muPt)
                if maxMuon_pt > 10:
                    self.histograms['signal/muon_pT'].Fill(maxMuon_pt)

            if row.nEle != 0:
                maxElectron_pt = max(row.elePt)
                if maxElectron_pt > 10:
                    self.histograms['signal/electron_pT'].Fill(maxElectron_pt)

            if row.nPho > 1:
                bestPts = heapq.nlargest(2,row.phoEt)
                if bestPts[0] > 15:
                    self.histograms['signal/photon1_pT'].Fill(bestPts[0])
                if bestPts[1] > 15:
                    self.histograms['signal/photon2_pT'].Fill(bestPts[1])
                
            
            # Figure out if we are in the peak or the sideband
            #if 80 < dimuon_mass < 110:
            #    # yes, the above syntax is correct, python is awesome
            #    self.histograms['signal/MyPtHistoName'].Fill(leg1_pt)
            #    self.histograms['signal/PtVsEta'].Fill(leg1_pt, row.m1Eta)
            #else:
            #    # sideband
            #    self.histograms['sideband/MyPtHistoName'].Fill(leg1_pt)

    def finish(self):
        ''' Write out your histograms, do fitting, etc... '''
        self.write_histos()
