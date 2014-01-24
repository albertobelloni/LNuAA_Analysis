from electron import electron
from muon import muon
from photon import photon

### MUON ID CUTS
def tight_muon_id(mu):
    return ( mu.isGlobalMuon() and mu.isPFMuon() and
             abs(mu.d0()) < 0.2 and abs(mu.dZ()) < 0.5 and
             mu.nValidPixelHits() > 0 and mu.nLayersWithMeasurement() > 5 and
             mu.globalChi2() < 10.0  and mu.nValidMuonHits() > 0 and
             mu.nMatchedStations() > 1 )

def loose_muon_iso(mu):
    # cHad + max(0, nHad+Pho - 0.5*cPart)
    return ( ( mu.chargedHadronIsoDR04() +
               max(0.0, ( mu.neutralHadronIsoDR04() + mu.photonIsoDR04() -
                          0.5*mu.puIsoDR04() ) )
               )/mu.pt() < 0.2 )


### ELECTRON ID CUTS
ele_sihih_cuts  = [0.10,0.30]
ele_dphiIN_cuts = [0.15,0.10]
ele_detaIN_cuts = [0.007,0.009]
ele_hovere_cuts = [0.12,0.10]
def electron_preselection(ele):
    eta_idx = 0
    thept = ele.pt()
    if( abs(ele.eta()) > 1.479 ): eta_idx += 1
    return ( abs(ele.d0()) < 0.02 and abs(ele.dZ()) < 0.1 and
             ele.missingHits() == 0 and
             ele.sigmaIEtaIEta() < ele_sihih_cuts[eta_idx] and
             ele.dPhiAtVtx() < ele_dphiIN_cuts[eta_idx] and
             ele.dEtaAtVtx() < ele_detaIN_cuts[eta_idx] and
             ele.HoverE() < ele_hovere_cuts[eta_idx] and
             ele.trackIsoDR03() / thept < 0.2 and
             ele.ecalIsoDR03()  / thept < 0.2 and
             ele.hcalIsoDR03()  / thept < 0.2 )
             

ele_mva_cuts = [[0.0,0.1,0.62],
                [0.94,0.85,0.92]]
def triggering_electron_id(ele):    
    if( ele.pt() < 10 ): return False
    if( ele.eta() > 2.5) : return False
    pt_idx = 0
    eta_idx = 0
    ele_eta = abs(ele.eta())
    if( ele.pt() >= 20 ): pt_idx+=1    
    if( ele_eta >= 0.8 ): eta_idx+=1
    if( ele_eta >= 1.479 ): eta_idx+=1
    return ele.kTrigMVA() > ele_mva_cuts[pt_idx][eta_idx]


ele_effective_areas_NHandPHO = [0.208,
                                0.209,
                                0.115,
                                0.143,
                                0.183,
                                0.194,
                                0.261]
ele_effective_area_cuts = [1.0,
                           1.479,
                           2.0,
                           2.2,
                           2.3,
                           2.4,
                           100.0]
def loose_electron_iso(ele):
    eta = abs(ele.eta())
    eta_idx = 0
    while( eta > ele_effective_area_cuts[eta_idx] ): eta_idx+=1
    EA = ele_effective_areas_NHandPHO[eta_idx]
    rho = ele._row.rho25_elePFiso
    return ( ( ele.chargedHadronIsoDR04() +
        max(0, ( ele.neutralHadronIsoDR04() + ele.photonIsoDR04() - rho*EA ) )
               )/ele.pt() < 0.2 )

### PHOTON ID CUTS


pho_sihih_cuts  = [0.012,0.034]
def loose_photon_id(pho):
    ebee = 0
    if( abs(pho.sc_eta()) > 1.479 ): ebee=1
    return ( pho.convSafeElectronVeto() == False and
             pho.towerHoverE() < 0.05  and
             pho.sigmaIEtaIEta() < pho_sihih_cuts[ebee] ) 
             

pho_effective_areas = [(0.012,0.030,0.148),
                       (0.010,0.057,0.130),
                       (0.014,0.039,0.112),
                       (0.012,0.015,0.216),
                       (0.016,0.024,0.262),
                       (0.020,0.039,0.260),
                       (0.012,0.072,0.266)]
pho_effective_area_cuts = [1.0,
                           1.479,
                           2.0,
                           2.2,
                           2.3,
                           2.4,
                           100.0]
pho_chad_iso_cut = [2.6,2.3]
pho_nhad_iso_cut = [(3.5,0.04),(2.9,0.04)]
pho_pho_iso_cut  = [(1.3,0.005),(1e6,0.0)]
def loose_photon_iso(pho):
    pt = pho.pt()
    eta = abs(pho.eta())
    ebee = 0
    if( abs(pho.sc_eta()) > 1.479 ): ebee=1
    eta_idx = 0
    while( eta > ele_effective_area_cuts[eta_idx] ): eta_idx+=1
    EA_ch  = pho_effective_areas[eta_idx][0]
    EA_neu = pho_effective_areas[eta_idx][1]
    EA_pho = pho_effective_areas[eta_idx][2]
    rho = pho._row.rho2012
    ch_corr_iso = max(0,pho.chargedHadronIsoDR03() - rho*EA_ch)
    neu_corr_iso = max(0,pho.neutralHadronIsoDR03() - rho*EA_neu)
    pho_corr_iso = max(0,pho.photonIsoDR03() - rho*EA_pho)
    chad_cut = pho_chad_iso_cut[ebee]
    nhad_cut = pho_nhad_iso_cut[ebee][0] + pt*pho_nhad_iso_cut[ebee][1]
    pho_cut  = pho_pho_iso_cut[ebee][0] + pt*pho_pho_iso_cut[ebee][1]
    return ( ch_corr_iso  < chad_cut and
             neu_corr_iso < nhad_cut and
             pho_corr_iso < pho_cut      )
