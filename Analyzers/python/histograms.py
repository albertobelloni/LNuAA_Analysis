from copy import deepcopy
from memoized import memoized


def fill_standard_histos(lepton,photon1,photon2,directory,hlist,histos):
    ### lepton plots
    histos[directory+'/lepton_pT'].Fill(lepton.pt())
    histos[directory+'/lepton_eta'].Fill(lepton.eta())
    ### leading plots
    histos[directory+'/photon1_pT'].Fill(photon1.pt())
    histos[directory+'/photon1_eta'].Fill(photon1.eta())
    if( abs(photon1.eta()) < 1.479 ):
        histos[directory+'/photon1_sihih_EB'].Fill(photon1.sigmaIEtaIEta())
        histos[directory+'/photon1_CHad_iso_EB'].Fill(photon1.chargedHadronIsoDR03())
        histos[directory+'/photon1_NHad_iso_EB'].Fill(photon1.neutralHadronIsoDR03())
        histos[directory+'/photon1_PFPho_iso_EB'].Fill(photon1.photonIsoDR03())
        histos[directory+'/photon1_PFPhoSCR_iso_EB'].Fill(photon1.photonSCRIsoDR04())
    else:
        histos[directory+'/photon1_sihih_EE'].Fill(photon1.sigmaIEtaIEta())
        histos[directory+'/photon1_CHad_iso_EE'].Fill(photon1.chargedHadronIsoDR03())
        histos[directory+'/photon1_NHad_iso_EE'].Fill(photon1.neutralHadronIsoDR03())
        histos[directory+'/photon1_PFPho_iso_EE'].Fill(photon1.photonIsoDR03())
        histos[directory+'/photon1_PFPhoSCR_iso_EE'].Fill(photon1.photonSCRIsoDR04())
    ### subleading
    histos[directory+'/photon2_pT'].Fill(photon2.pt())
    histos[directory+'/photon2_eta'].Fill(photon2.eta())
    if( abs(photon2.eta()) < 1.479 ):
        histos[directory+'/photon2_sihih_EB'].Fill(photon2.sigmaIEtaIEta())
        histos[directory+'/photon2_CHad_iso_EB'].Fill(photon2.chargedHadronIsoDR03())
        histos[directory+'/photon2_NHad_iso_EB'].Fill(photon2.neutralHadronIsoDR03())
        histos[directory+'/photon2_PFPho_iso_EB'].Fill(photon2.photonIsoDR03())
        histos[directory+'/photon2_PFPhoSCR_iso_EB'].Fill(photon2.photonSCRIsoDR04())
    else:
        histos[directory+'/photon2_sihih_EE'].Fill(photon2.sigmaIEtaIEta())
        histos[directory+'/photon2_CHad_iso_EE'].Fill(photon2.chargedHadronIsoDR03())
        histos[directory+'/photon2_NHad_iso_EE'].Fill(photon2.neutralHadronIsoDR03())
        histos[directory+'/photon2_PFPho_iso_EE'].Fill(photon2.photonIsoDR03())
        histos[directory+'/photon2_PFPhoSCR_iso_EE'].Fill(photon2.photonSCRIsoDR04())

def fill_dilepton_histos(lepton1,lepton2,directory,hlist,histos):
    pass

def fill_llg_histos(lepton1,lepton2,photon,directory,hlist,histos):
    pass

_lepton_histograms = [('lepton_pT','p_{T} (GeV)', 470, 30, 500),
                      ('lepton_eta','#eta',200,-2.5,2.5)]

_photon1_histograms = [('photon1_pT','Leading Photon p_{T} (GeV)',485,15,500),
                       ('photon1_eta','Leading Photon #eta',200,-2.5,2.5),
                       ('photon1_sihih_EB','Barrel Leading Photon #sigma_{i#etai#eta}',0,0.05),
                       ('photon1_sihih_EE','Endcaps Leading Photon #sigma_{i#etai#eta}',0,0.05),
                       ('photon1_CHad_iso_EB','1^{st} Barrel Photon Charged Hadron Iso. (GeV)',40,0,20),
                       ('photon1_CHad_iso_EE','1^{st} Endcap Photon Charged Hadron Iso. (GeV)',40,0,20),
                       ('photon1_NHad_iso_EB','1^{st} Barrel Photon Neutral Hadron Iso. (GeV)',40,0,20),
                       ('photon1_NHad_iso_EE','1^{st} Endcap Photon Neutral Hadron Iso. (GeV)',40,0,20),
                       ('photon1_PFPho_iso_EB','1^{st} Photon Neutral EM Iso. (GeV)',40,0,20),
                       ('photon1_PFPho_iso_EE','1^{st} Endcap Photon Neutral EM Iso. (GeV)',40,0,20),
                       ('photon1_PFPhoSCR_iso_EB','1^{st} Barrel Photon Neutral Footprint-removed EM Iso. (GeV)',200,0,20)
                       ('photon1_PFPhoSCR_iso_EE','1^{st} Endcap Photon Neutral Footprint-removed EM Iso. (GeV)',200,0,20)]

_photon2_histograms = [('photon2_pT','Sub-leading Photon p_{T} (GeV)',485,15,500),
                       ('photon2_eta','Sub-leading Photon #eta',200,-2.5,2.5),
                       ('photon2_sihih_EB','Barrel Sub-leading Photon #sigma_{i#etai#eta}',0,0.05),
                       ('photon2_sihih_EE','Endcaps Sub-leading Photon #sigma_{i#etai#eta}',0,0.05),
                       ('photon2_CHad_iso','2^{nd} Photon Charged Hadron Iso. (GeV)',40,0,20),
                       ('photon2_NHad_iso','2^{nd} Photon Neutral Hadron Iso. (GeV)',40,0,20),
                       ('photon2_PFPho_iso','2^{nd} Photon Neutral EM Iso. (GeV)',40,0,20),
                       ('photon2_PFPhoSCR_iso','2^{nd} Photon Footprint-removed Neutral EM Iso. (GeV)',200,0,20)]

_diphoton_histograms = [('dipho_mass','Di-#gamma Mass (GeV)',500,0,500),
                        ('dipho_pt','Di-#gamma p_{T} (GeV)',500,0,500),
                        ('dipho_dr','Di-#gamma #DeltaR',200,0,6)]

_pho1lep_histograms = [('lep_pho1_mass','Lepton + Leading #gamma Mass (GeV)',500,0,500),
                       ('lep_pho1_mass','Lepton - Leading #gamma #DeltaR',200,0,6)]

_pho2lep_histograms = [('lep_pho2_mass','Lepton + Subleading #gamma Mass (GeV)',500,0,500),
                       ('lep_pho2_mass','Lepton - Subleading #gamma #DeltaR',200,0,6)]

_lepdipho_histograms = [('lep_dipho_vismass','W#gamma#gamma Visible Mass (GeV)',1000,0,1000),
                        ('lep_dipho_mT','W#gamma#gamma Transverse Mass (GeV)'1000,0,1000),
                        ('leppho1_vs_leppho2_mass','m_{l#gamma^{1}} (GeV)','m_{l#gamma^{2} (GeV)',100,0,1000,100,0,1000)]

_histos = ( _lepton_histograms   + _photon1_histograms + _photon2_histograms +
            _diphoton_histograms + _pho1lep_histograms + _pho2lep_histograms +
            _lepdipho_histograms )

_dileptonhistos = [('dilep_mass','Di-lepton Invariant Mass (GeV)',1000,0,1000)]

_llghistos = [('llg_mass','Di-lepton + #gamma Invariant Mass (GeV)',1000,0,1000)]

#blinded analysis
blind_histograms = {
    'muon/sidebands/one_sihih_inverted':deepcopy(_histos),
    'muon/sidebands/two_sihih_inverted':deepcopy(_histos),
    'muon/sidebands/one_pfphoton_iso_inverted':deepcopy(_histos),
    'muon/sidebands/two_pfphoton_iso_inverted':deepcopy(_histos),
    'muon/sidebands/lepton_veto':deepcopy(_histos),
    'muon/sidebands/dilepton_gamma':deepcopy(_dileptonhistos),
    'muon/sidebands/dilepton':deepcopy(_llghistos),
    'electron/sidebands/one_sihih_inverted':deepcopy(_histos),
    'electron/sidebands/two_sihih_inverted':deepcopy(_histos),
    'electron/sidebands/one_pfphoton_iso_inverted':deepcopy(_histos),
    'electron/sidebands/two_pfphoton_iso_inverted':deepcopy(_histos),
    'electron/sidebands/lepton_veto':deepcopy(_histos),
    'electron/sidebands/dilepton':deepcopy(_dileptonhistos),
    'electron/sidebands/dilepton_gamma':deepcopy(_llghistos)
    }

#unblinded analysis
unblind_histograms = {
    'muon/signal/all_pog_cuts':deepcopy(_histos),
    'muon/signal/no_pfphoton_iso':deepcopy(_histos),
    'muon/signal/no_sihih':deepcopy(_histos),
    'muon/sidebands/one_sihih_inverted':deepcopy(_histos),
    'muon/sidebands/two_sihih_inverted':deepcopy(_histos),
    'muon/sidebands/one_pfphoton_iso_inverted':deepcopy(_histos),
    'muon/sidebands/two_pfphoton_iso_inverted':deepcopy(_histos),
    'muon/sidebands/lepton_veto':deepcopy(_histos),
    'muon/sidebands/dilepton':deepcopy(_dileptonhistos),
    'muon/sidebands/dilepton_gamma':deepcopy(_llghistos),
    'electron/signal/all_pog_cuts':deepcopy(_histos),
    'electron/signal/no_pfphoton_iso':deepcopy(_histos),
    'electron/signal/no_sihih':deepcopy(_histos),
    'electron/sidebands/one_sihih_inverted':deepcopy(_histos),
    'electron/sidebands/two_sihih_inverted':deepcopy(_histos),
    'electron/sidebands/one_pfphoton_iso_inverted':deepcopy(_histos),
    'electron/sidebands/two_pfphoton_iso_inverted':deepcopy(_histos),
    'electron/sidebands/lepton_veto':deepcopy(_histos),
    'electron/sidebands/dilepton':deepcopy(_dileptonhistos),
    'electron/sidebands/dilepton_gamma':deepcopy(_llghistos)
    }
