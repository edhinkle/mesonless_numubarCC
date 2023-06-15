import matplotlib
import matplotlib.pyplot as plt
import h5py
import glob
import json
import argparse
import numpy as np
import twoBytwo_defs
import auxiliary
import signal_characterization as sig_char

# PLOT: Hadron kinematics
#       sig_bkg is an int such that 0 == signal, 1 == 'dirt' backgrounds, 2 == 'beam' backgrounds
def plot_hadrons(d, scale_factor, sig_bkg = 0):
    
    # DEFINE: Plotting muon kinematics for signal or background events
    sample_type = ''
    sample_title = ''
    if sig_bkg == 0: 
        sample_type = 'signal'
        sample_title = 'Signal'
    elif sig_bkg == 1:
        sample_type = 'dirt_bkg'
        sample_title = 'Dirt Background'
    elif sig_bkg == 2:
        sample_type = 'beam_bkg'
        sample_title = 'Beam Background'
    else: 
        return "Error: plot_hadrons function given undefined signal/background definition"
    
    # PLOT: total visible energy + contained visible energy
    fig0, ax0 = plt.subplots(figsize=(8,4))
    data0tot = np.array([d[key]['total_edep'] for key in d.keys()])
    #data0cont = np.array([d[key]['contained_edep'] for key in d.keys()])
    counts0tot, bins0tot = np.histogram(data0tot, bins=np.linspace(0,800,40))
    #counts0cont, bins0cont = np.histogram(data0cont, bins=np.linspace(0,800,40))
    ax0.hist(bins0tot[:-1], bins=bins0tot, weights = counts0tot*scale_factor, label='Total', histtype='step')
    #ax0.hist(bins0cont[:-1], bins=bins0cont, weights = counts0cont*scale_factor, label='Contained',histtype='step', linestyle='--')
    ax0.set_xlabel('Total Visible Hadron Energy [MeV]')
    ax0.set_ylabel('Count / 20 MeV')
    ax0.set_yscale('log')
    #ax0.legend()
    ax0.grid(True)
    plt.savefig(sample_type+"_events_hadron_visible_energy.png")
    plt.close(fig0)

    # PLOT: hadron energy containment fraction ## UNNECESSARY PLOT AT THE MOMENT
    fig1, ax1 = plt.subplots(figsize=(6,4))
    data1 = np.array([d[key]['contained_edep']/d[key]['total_edep'] for key in d.keys() if d[key]['total_edep']!=0])
    counts1, bins1 = np.histogram(data1, bins=np.linspace(0,1,20))
    ax1.hist(bins1[:-1], bins=bins1, weights = counts1*scale_factor, histtype='step')
    ax1.set_xlabel('Visible Hadron Energy Containment Fraction')
    ax1.set_ylabel('Count / 0.05')
    ax1.grid(True)       
    ax0.set_yscale('log')
    plt.savefig(sample_type+"_events_hadron_energy_containment_fraction.png")
    plt.close(fig1)

    # PLOT: hadron multiplicity
    fig2, ax2 = plt.subplots(figsize=(6,4))
    data2 = np.array([d[key]['hadron_mult'] for key in d.keys()])
    counts2, bins2 =np.histogram(data2, bins=np.linspace(0,25,26))
    ax2.hist(bins2[:-1], bins=bins2, weights = counts2*scale_factor, histtype='step')
    ax2.set_xlabel(r"Primary Hadron Multiplicity")
    ax2.set_ylabel("Count / Hadron") 
    plt.savefig(sample_type+"_events_hadron_multiplicity_truth.png")
    plt.close(fig2)    

    # PLOT: truth-level 4-momentum squared of interaction
    #       ** no scale factor applied because we're looking at fractions anyways ** 
    fig3, ax3 = plt.subplots(figsize=(6,4))
    hadron_fs_pdg_list=[sorted(d[key]['hadron_pdg_set']) for key in d.keys()]
    hadron_fs_pdg_set=set(tuple(pdg) for pdg in hadron_fs_pdg_list)
    #print("Hadron PDG List:", hadron_fs_pdg_list)
    #print("Hadron PDG Set:", hadron_fs_pdg_set)
    hadron_fs_pdg_count=[(pdg_set, hadron_fs_pdg_list.count(list(pdg_set))) for pdg_set in hadron_fs_pdg_set]
    hadron_fs_pdg_fraction=[100*(i[1]/len(data2)) for i in hadron_fs_pdg_count]
    hadron_fs_pdg_labels=['+'.join(str(auxiliary.hadron_pdg_dict[j]) for j in i[0]) for i in hadron_fs_pdg_count]
    #print("Number of Events:", len(hadron_fs_pdg_list))
    #print("Hadron FS PDG Count:", hadron_fs_pdg_count)
    #print("Hadron FS PDG Fractions:", hadron_fs_pdg_fraction)
    #print("Hadron FS PDG Labels:", hadron_fs_pdg_labels)
    ax3.pie(hadron_fs_pdg_fraction, labels=hadron_fs_pdg_labels, autopct='%1.1f%%')
    ax3.set_title(r"Final State Hadrons in "+sample_title+" Events")
    plt.savefig(sample_type+"_events_hadron_pdg_ids_truth.png")
    plt.close(fig3)    

    # PLOT: other hadron multiplicity
    fig4, ax4 = plt.subplots(figsize=(6,4))
    data4 = np.array([d[key]['other_had_mult'] for key in d.keys()])
    counts4, bins4 =np.histogram(data4, bins=np.linspace(0,10,11))
    ax4.hist(bins4[:-1], bins=bins4, weights = counts4*scale_factor, histtype='step')
    ax4.set_xlabel(r"Other Primary Hadron Multiplicity")
    ax4.set_ylabel("Count / Other Hadron") 
    plt.savefig(sample_type+"_events_other_hadron_multiplicity_truth.png")
    plt.close(fig4)    

    # PLOT: neutron multiplicity
    fig5, ax5 = plt.subplots(figsize=(6,4))
    data5 = np.array([d[key]['neutron_mult'] for key in d.keys()])
    counts5, bins5 =np.histogram(data5, bins=np.linspace(0,20,21))
    ax5.hist(bins5[:-1], bins=bins5, weights = counts5*scale_factor, histtype='step')
    ax5.set_xlabel(r"Primary Neutron Multiplicity")
    ax5.set_ylabel("Count / Neutron") 
    plt.savefig(sample_type+"_events_neutron_multiplicity_truth.png")
    plt.close(fig5)    

    # PLOT: proton multiplicity
    fig6, ax6 = plt.subplots(figsize=(6,4))
    data6 = np.array([d[key]['proton_mult'] for key in d.keys()])
    counts6, bins6 =np.histogram(data6, bins=np.linspace(0,20,21))
    ax6.hist(bins6[:-1], bins=bins6, weights = counts6*scale_factor, histtype='step')
    ax6.set_xlabel(r"Primary Proton Multiplicity")
    ax6.set_ylabel("Count / Proton") 
    plt.savefig(sample_type+"_events_proton_multiplicity_truth.png")
    plt.close(fig6)   

    
    # PLOT: Fractions of Events with diff numbers of protons
    #       ** no scale factor applied because we're looking at fractions anyways ** 
    fig7, ax7 = plt.subplots(figsize=(6,4))
    p_mult_list = []
    total_np_events = 0
    for key in d.keys():
        if d[key]['other_had_mult']==0 and d[key]['proton_mult']>0 and d[key]['neutron_mult']>0:
            p_mult_list.append(d[key]['proton_mult'])
            total_np_events+=1
    if total_np_events >0:
        p_mult_count=[(mult_count, p_mult_list.count(mult_count)) for mult_count in np.arange(np.max(np.array(p_mult_list)))]
        #print("P mult count:", p_mult_count)
        p_mult_fraction=[100*(i[1]/total_np_events) for i in p_mult_count if i[1]>0 and i[0]<6]
        p_mult_labels=[str(i[0]) for i in p_mult_count if i[1]>0 and i[0]<6]
        many_p = 0
        for num, count in p_mult_count:
            if num < 6: continue
            if count==0: continue
            many_p+=count
        p_mult_fraction.append(100*(many_p/total_np_events))
        p_mult_labels.append('>5')
        #print("P mult labels:", p_mult_labels)
        ax7.pie(p_mult_fraction, labels=p_mult_labels, autopct='%1.1f%%')
        ax7.set_title(r"Primary Proton Multiplicity in "+sample_title+"\nEvents with Neutrons and Protons")
        plt.savefig(sample_type+"_events_proton_mult_in_pn_events_truth.png")
    plt.close(fig7)    

    # PLOT: Max proton length for n p events
    fig8, ax8 = plt.subplots(figsize=(8,4))
    p_tot_lens = []
    #p_cont_lens = []
    events_w_protons = 0
    for key in d.keys():
        if d[key]['proton_mult']>0:
            p_tot_lens.append(d[key]['max_p_total_length'])
            #p_cont_lens.append(d[key]['max_p_contained_length'])
            events_w_protons+=1
    if events_w_protons >0:  
        data8tot = np.array(p_tot_lens)
        #data8cont = np.array(p_cont_lens)
        counts8tot, bins8tot = np.histogram(data8tot, bins=np.linspace(0,60,60))
        #counts8cont, bins8cont = np.histogram(data8cont, bins=np.linspace(0,60,60))
        ax8.hist(bins8tot[:-1], bins=bins8tot, weights = counts8tot*scale_factor, label='Total', histtype='step')
        #ax8.hist(bins8cont[:-1], bins=bins8cont, weights = counts8cont*scale_factor, label='Contained',histtype='step', linestyle='--')
        ax8.set_xlabel(r"Length [cm]")
        ax8.set_title("Length of Longest Proton Track in "+sample_title+" Events with Neutrons and Protons")
        ax8.set_ylabel("Events / cm") 
        #ax8.legend()
        plt.savefig(sample_type+"_events_max_proton_length_in_pn_events_truth.png")   
    plt.close(fig8)

    # PLOT: hadron multiplicity above threshold
    fig9, ax9 = plt.subplots(figsize=(6,4))
    data9 = np.array([d[key]['hadron_mult_over_thresh'] for key in d.keys()])
    counts9, bins9 =np.histogram(data9, bins=np.linspace(0,12,13))
    ax9.hist(bins9[:-1], bins=bins9, weights = counts9*scale_factor, histtype='step')
    ax9.set_xlabel(r"Primary Hadron Multiplicity Above Threshold")
    ax9.set_ylabel("Events / Hadron") 
    plt.savefig(sample_type+"_events_hadron_multiplicity_above_threshold.png")
    plt.close(fig9)  

    # PLOT: proton multiplicity above threshold
    fig10, ax10 = plt.subplots(figsize=(6,4))
    data10 = np.array([d[key]['proton_mult_over_thresh'] for key in d.keys()])
    counts10, bins10 =np.histogram(data10, bins=np.linspace(0,12,13))
    ax10.hist(bins10[:-1], bins=bins10, weights = counts10*scale_factor, histtype='step')
    ax10.set_xlabel(r"Primary Proton Multiplicity Above Threshold")
    ax10.set_ylabel("Events / Proton") 
    plt.savefig(sample_type+"_events_proton_multiplicity_above_threshold.png")
    plt.close(fig10)   

    # PLOT: Lead proton momentum for events with protons
    fig11, ax11 = plt.subplots(figsize=(8,4))
    p_lead_mom = []
    events_w_protons = 0
    for key in d.keys():
        if d[key]['proton_mult_over_thresh']>0:
            p_lead_mom.append(d[key]['lead_proton_momentum'])
            events_w_protons+=1
    if events_w_protons >0:  
        data11tot = np.array(p_lead_mom)
        counts11tot, bins11tot = np.histogram(data11tot, bins=np.linspace(0,2000,41))
        ax11.hist(bins11tot[:-1], bins=bins11tot, weights = counts11tot*scale_factor, histtype='step')
        ax11.set_xlabel(r"Momentum [MeV/c]")
        ax11.set_title("Leading Proton Momentum in\n"+sample_title+" Events with Protons Above Threshold")
        ax11.set_ylabel("Events / 50 MeV/c") 
        plt.savefig(sample_type+"_lead_proton_momentum_events_with_protons_above_threshold.png")   
    plt.close(fig11)

    # PLOT: Sub-leading proton momentum for events with 2+ protons
    fig12, ax12 = plt.subplots(figsize=(8,4))
    p_sublead_mom = []
    events_w_greq_2_protons = 0
    for key in d.keys():
        if d[key]['proton_mult_over_thresh']>1:
            p_sublead_mom.append(d[key]['sub_lead_proton_momentum'])
            events_w_greq_2_protons+=1
    if events_w_greq_2_protons >0:  
        data12tot = np.array(p_sublead_mom)
        counts12tot, bins12tot = np.histogram(data12tot, bins=np.linspace(0,2000,41))
        ax12.hist(bins12tot[:-1], bins=bins12tot, weights = counts12tot*scale_factor, histtype='step')
        ax12.set_xlabel(r"Momentum [MeV/c]")
        ax12.set_title("Subleading Proton Momentum in \n"+sample_title\
                       +" Events with 2+ Protons Above Threshold")
        ax12.set_ylabel("Events / 50 MeV/c") 
        plt.savefig(sample_type+"_sublead_proton_momentum_events_with_greq_2_protons_above_threshold.png")   
    plt.close(fig12)

    # PLOT: Lead proton angle wrt beam for events with protons
    fig13, ax13 = plt.subplots(figsize=(8,4))
    p_lead_ang_wrt_beam = []
    events_w_protons = 0
    for key in d.keys():
        if d[key]['proton_mult_over_thresh']>0:
            p_lead_ang_wrt_beam.append(d[key]['lead_proton_ang_wrt_beam'])
            events_w_protons+=1
    if events_w_protons >0:  
        data13tot = np.array(p_lead_ang_wrt_beam)
        counts13tot, bins13tot = np.histogram(data13tot, bins=np.linspace(0,3.2,33))
        ax13.hist(bins13tot[:-1], bins=bins13tot, weights = counts13tot*scale_factor, histtype='step')
        ax13.set_xlabel(r"Angle [Rad]")
        ax13.set_title("Leading Proton Angle with respect to Beam Direction in\n"+sample_title\
                       +" Events with Protons Above Threshold")
        ax13.set_ylabel("Events / 0.1 Rad") 
        plt.savefig(sample_type+"_lead_proton_angle_wrt_beam_direction_events_with_protons_above_threshold.png")   
    plt.close(fig13)

    # PLOT: Subleading proton angle wrt beam for events with protons
    fig14, ax14 = plt.subplots(figsize=(8,4))
    p_sublead_ang_wrt_beam = []
    events_w_greq_2_protons = 0
    for key in d.keys():
        if d[key]['proton_mult_over_thresh']>1:
            p_sublead_ang_wrt_beam.append(d[key]['sub_lead_proton_ang_wrt_beam'])
            events_w_greq_2_protons+=1
    if events_w_greq_2_protons >0:  
        data14tot = np.array(p_sublead_ang_wrt_beam)
        counts14tot, bins14tot = np.histogram(data14tot, bins=np.linspace(0,3.2,33))
        ax14.hist(bins14tot[:-1], bins=bins14tot, weights = counts14tot*scale_factor, histtype='step')
        ax14.set_xlabel(r"Angle [Rad]")
        ax14.set_title("Subleading Proton Angle with respect to Beam Direction in\n"+sample_title\
                       +" Events with 2+ Protons Above Threshold")
        ax14.set_ylabel("Events / 0.1 Rad") 
        plt.savefig(sample_type+"_sublead_proton_angle_wrt_beam_direction_events_with_greq_2_protons_above_threshold.png")   
    plt.close(fig14)

    # PLOT: Subleading proton angle wrt beam for events with protons
    fig15, ax15 = plt.subplots(figsize=(8,4))
    p_sublead_ang_wrt_lead_proton = []
    events_w_greq_2_protons = 0
    for key in d.keys():
        if d[key]['proton_mult_over_thresh']>1:
            p_sublead_ang_wrt_lead_proton.append(d[key]['sub_lead_proton_angle_with_lead_proton'])
            events_w_greq_2_protons+=1
    if events_w_greq_2_protons >0:  
        data15tot = np.array(p_sublead_ang_wrt_lead_proton)
        counts15tot, bins15tot = np.histogram(data15tot, bins=np.linspace(0,1.6,17))
        ax15.hist(bins15tot[:-1], bins=bins15tot, weights = counts15tot*scale_factor, histtype='step')
        ax15.set_xlabel(r"Angle [Rad]")
        ax15.set_title("Subleading Proton Angle with respect to Leading Proton Direction\n in "+sample_title \
                       +" Events with 2+ Protons Above Threshold")
        ax15.set_ylabel("Events / 0.1 Rad") 
        plt.savefig(sample_type+"_sublead_proton_angle_wrt_lead_proton_events_with_greq_2_protons_above_threshold.png")   
    plt.close(fig15)

    # PLOT: proton multiplicity truth vs. over threshold
    fig16, ax16 = plt.subplots(figsize=(6,4))
    data16_tr = np.array([d[key]['proton_mult'] for key in d.keys()])
    data16_thresh= np.array([d[key]['proton_mult_over_thresh'] for key in d.keys()])
    counts16_tr, bins16_tr =np.histogram(data16_tr, bins=np.linspace(0,20,21))
    counts16_thresh, bins16_thresh =np.histogram(data16_thresh, bins=np.linspace(0,20,21))
    ax16.hist(bins16_tr[:-1], bins=bins16_tr, weights = counts16_tr*scale_factor, label="Truth", histtype='step')
    ax16.hist(bins16_thresh[:-1], bins=bins16_thresh, weights = counts16_thresh*scale_factor, label="Over Threshold", histtype='step', linestyle='--')
    ax16.set_xlabel(r"Primary Proton Multiplicity")
    ax16.set_ylabel("Events / Proton") 
    plt.legend()
    plt.savefig(sample_type+"_events_proton_multiplicity_truth_vs_over_threshold.png")
    plt.close(fig16)   

    # PLOT: Primary Proton K.E. for events with Protons Over Threshold
    fig17, ax17 = plt.subplots(figsize=(8,4))
    p_ke = []
    events_w_protons = 0
    for key in d.keys():
        if d[key]['proton_mult_over_thresh']>0:
            p_ke.append(d[key]['primary_protons_total_ke'])
            events_w_protons+=1
    if events_w_protons >0:  
        data17tot = np.array(p_ke)
        counts17tot, bins17tot = np.histogram(data17tot, bins=np.linspace(0,2000,41))
        ax17.hist(bins17tot[:-1], bins=bins17tot, weights = counts17tot*scale_factor, histtype='step')
        ax17.set_xlabel(r"Kinetic Energy [MeV]")
        ax17.set_title("Total Primary Proton Kinetic Energy in\n"+sample_title+" Events with Protons Over Threshold")
        ax17.set_ylabel("Events / 50 MeV") 
        plt.savefig(sample_type+"_primary_proton_ke_events_with_protons_above_threshold.png")   
    plt.close(fig17)

    # PLOT: Truth KE vs. Contained KE for primary protons
    fig18, ax18 = plt.subplots(figsize=(8,4))
    data18tot = np.array([d[key]['primary_protons_total_ke'] for key in d.keys()])
    data18cont = np.array([d[key]['contained_edep_over_thresh'] for key in d.keys()])
    counts18tot, bins18tot = np.histogram(data18tot, bins=np.linspace(0,2000,101))
    counts18cont, bins18cont = np.histogram(data18cont, bins=np.linspace(0,2000,101))
    ax18.hist(bins18tot[:-1], bins=bins18tot, weights = counts18tot*scale_factor, label='Total', histtype='step')
    ax18.hist(bins18cont[:-1], bins=bins18cont, weights = counts18cont*scale_factor, label='Contained',histtype='step', linestyle='--')
    ax18.set_xlabel('Primary Proton Energy [MeV]')
    ax18.set_ylabel('Events / 20 MeV')
    ax18.set_yscale('log')
    ax18.legend()
    plt.savefig(sample_type+"_events_primary_proton_truth_ke_vs_contained_ke.png")
    plt.close(fig18)