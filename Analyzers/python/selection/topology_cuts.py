"""
Definitions of topology cuts (like cross cleaning and such)
"""

import ROOT
from ROOT import TVector2

from math import hypot

def cross_clean(to_clean,cleaning_against,DRCut=0.4):
    for clean_obj in cleaning_against:
        deta = to_clean.eta() - clean_obj.eta()
        dphi = TVector2.Phi_mpi_pi(to_clean.phi() - clean_obj.phi())
        if hypot(deta,dphi) < DRCut:
            return False
    return True

def in_ecal_fiducial(egobj):
    absEta = abs(egobj.eta())
    return ( absEta < 1.4442 or ( absEta > 1.560 and absEta < 2.5 ) )
                     
        
        
