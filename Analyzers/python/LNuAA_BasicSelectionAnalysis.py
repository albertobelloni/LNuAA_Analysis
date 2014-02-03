"""
a baseline implementation of the LNuAA analysis that stores signal and siebands
"""

import heapq
# import the MegaBase class
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

#get analysis object classes
from LNuAA_Analysis.Analyzers.selection.electron import electron
from LNuAA_Analysis.Analyzers.selection.muon import muon
from LNuAA_Analysis.Analyzers.selection.photon import photon

# get some helper functions
from LNuAA_Analysis.Analyzers.selection.topology_cuts import cross_clean, \
     in_ecal_fiducial

from LNuAA_Analysis.Analyzers.selection.object_id_cuts import tight_muon_id, \
     loose_muon_iso, electron_preselection, triggering_electron_id, \
     loose_electron_iso, loose_photon_id, loose_photon_iso

# Import various other code used by this module
# We need this because of the "type = ROOT.TH2F" below
import ROOT

# define our analyzer class - it must be called MyAnalyzer, since that is
# the name of this file.  It inherits from MegaBase.
class LNuAA_BasicSelectionAnalysis(MegaBase):
    # We have to define the path that the target ntuple can be found.
    tree = 'ggNtuplizer/EventTree'

    def __init__(self, tree, outputfile, **kwargs):
        MegaBase.__init__(self,tree,outputfile,**kwargs)
        """
        The __init__ method must take the following arguments:

        tree:       a ROOT TTree that will be processed.
        outputfile: a ROOT TFile (already open) to write output into
        **kwargs:   optionally extra keyword args can be passed (advanced)
        """
        self.tree = tree  # need to keep a reference to this for later
        self.outputfile = outputfile
        

    def begin(self):
        """ Let's book some histograms.

        This is configured for four total regions:
        electron : signal / sideband
        muon : signal / sideband

        The histograms are available via a dictionary called "histograms".

        The keys of the dictionary are the full paths to the histograms.

        """

        # MegaBase includes some convenience methods for booking histograms.
        # This books a 200 bin TH1F called "MyHistoName" into the "signal"
        # folder.
        self.book('mu_signal', 'muon_pT', 'p_{T}', 200, 10, 110)
        self.book('mu_signal', 'muon_eta', '#eta', 200, -2.4, 2.4) 
        self.book('mu_signal', 'photon1_pT', 'p_{T}', 200, 10, 110)
        self.book('mu_signal', 'photon1_eta', 'p_{T}', 200, -2.5, 2.5)
        self.book('mu_signal', 'photon2_pT', 'p_{T}', 200, 10, 110)
        self.book('mu_signal', 'photon2_eta', 'p_{T}', 200, -2.5, 2.5)

        self.book('el_signal', 'electron_pT', 'p_{T}', 200, 10, 110)
        self.book('el_signal', 'electron_eta', '#eta', 200, -2.5, 2.5) 
        self.book('el_signal', 'photon1_pT', 'p_{T}', 200, 10, 110)
        self.book('el_signal', 'photon1_eta', 'p_{T}', 200, -2.5, 2.5)
        self.book('el_signal', 'photon2_pT', 'p_{T}', 200, 10, 110)
        self.book('el_signal', 'photon2_eta', 'p_{T}', 200, -2.5, 2.5)

        # How to make a 2D histo
        #self.book('signal', 'PtVsEta', 'p_{T} vs. #eta',
        #          200, 0, 100, 100, -2.5, 2.5, type=ROOT.TH2F)

        # In our sideband
        #self.book('sideband', 'MyPtHistoName', 'p_{T}', 200, 0, 100)

    def process(self):
        """ Our analysis logic. """
        # Loop over the tree
        for row in self.tree:
            if( row.muEta.size() != row.nMu or
                row.eleEta.size() != row.nEle or
                row.phoEta.size() != row.nPho ):
                continue
            # skip events that don't have any basic objects
            if( row.nMu == 0 and row.nEle == 0 and row.nPho < 2 ):
                continue
            
            #create basic lists of muons/electrons/photons
            electrons = [electron(row,iel) for iel in xrange(row.nEle)]
            muons = [muon(row,imu) for imu in xrange(row.nMu)]
            photons = [photon(row,ipho) for ipho in xrange(row.nPho)]

            if( self.event_veto_mc_photon(photons) ): continue

            # select leptons            
            muons = filter(lambda x : x.pt() > 7, muons)
            muons = filter(tight_muon_id, muons)
            count_muons_id = len(muons)

            electrons = filter(lambda x : x.pt() > 7, electrons)
            electrons = filter(electron_preselection, electrons)
            electrons = filter(triggering_electron_id, electrons)
            count_electrons_id = len(electrons)            

            ### loose lepton veto, don't isolate here since we need
            ### the veto to be discriminating against crappy leptons
            if( count_muons_id + count_electrons_id > 1 ): continue

            #we want isolated electrons
            muons = filter(loose_muon_iso, muons)
            electrons = filter(loose_electron_iso, electrons)
            
            # also kill photons that overlap with a selected electrons
            photons = filter(lambda x : cross_clean(x,electrons), photons)

            #cut on the lepton pT
            electrons = filter(lambda x : x.pt() > 30, electrons)
            muons = filter(lambda x : x.pt() > 30, muons)

            if len(electrons) == 0 and len(muons) == 0:
                continue

            #cut on the lepton eta
            electrons = filter(lambda x : abs(x.eta()) < 2.5, electrons)
            muons = filter(lambda x : abs(x.eta()) < 2.4, muons)

            if len(electrons) == 0 and len(muons) == 0:
                continue

            #filter out the photons we will not consider
            # pt lower than 15, outside of ECAL fiducial
            photons = filter(lambda x : x.pt() > 15, photons)
            photons = filter(in_ecal_fiducial, photons)
            photons = filter(loose_photon_id, photons)
            photons = filter(loose_photon_iso, photons)

            if len(photons) < 2:
                continue
            
            #sort selected objects descending in pT
            electrons = sorted(electrons,key=lambda x : x.pt(), reverse=True)
            muons = sorted(muons,key=lambda x : x.pt(), reverse=True)
            photons = sorted(photons,key=lambda x : x.pt(), reverse=True)

            if len(muons):
                self.histograms['mu_signal/muon_pT'].Fill(muons[0].pt())
                self.histograms['mu_signal/muon_eta'].Fill(muons[0].eta())
                self.histograms['mu_signal/photon1_pT'].Fill(photons[0].pt())
                self.histograms['mu_signal/photon1_eta'].Fill(photons[0].eta())
                self.histograms['mu_signal/photon2_pT'].Fill(photons[1].pt())
                self.histograms['mu_signal/photon2_eta'].Fill(photons[1].eta())
            if len(electrons):
                self.histograms['el_signal/electron_pT'].Fill(electrons[0].pt())
                self.histograms['el_signal/electron_eta'].Fill(electrons[0].eta())
                self.histograms['el_signal/photon1_pT'].Fill(photons[0].pt())
                self.histograms['el_signal/photon1_eta'].Fill(photons[0].eta())
                self.histograms['el_signal/photon2_pT'].Fill(photons[1].pt())
                self.histograms['el_signal/photon2_eta'].Fill(photons[1].eta())
                

    def event_veto_mc_photon(self,phos):
        return False

    def finish(self):
        """ Write out your histograms, do fitting, etc... """
        self.write_histos()
