# script to get and plot TTS for campaign average conditions, varying tau 
# date created: 2/16/2020
# author: sofia chelpon

############################ PREP WORKSPACE ############################
import numpy as np 
import pandas as pd

import matplotlib
from matplotlib import pyplot as plt

# import my TTS module, need to add path to folder
import sys
sys.path.insert(1, '/UTLS/schelpon/TTS_2020/base_tts_code/')
import tts_mod

# read in ratios dataframe
contrast_ratios = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/contrast_ratios.pkl")
ratios_sort = contrast_ratios.sort_values(['BL_tau'])
ratios_sort.head()

# utbl, same for all 
utbl = ratios_sort['All RF']

############################ GET TTS OUTPUTS FOR EA. CASE ############################
# --------------- ver 1: BL TAU 
tau_bl = ratios_sort['BL_tau'].values

# get inputs
t_bl, exp_decay_matrix_bl, LT_bl = tts_mod.prep_for_tts(tau_bl)
# get tts 
my_mustar_bl, my_r2_bl, my_gf_bl, my_t_bl, mean_age_bl, mode_age_bl, best_k_bl = tts_mod.get_tts(utbl, tau_bl, t_bl, exp_decay_matrix_bl, LT_bl)

# save campaign average for later use 
campaign_avg_figa = pd.DataFrame()
campaign_avg_figa['tau'] = tau_bl
campaign_avg_figa['utbl'] = utbl.values
campaign_avg_figa['mustar'] = my_mustar_bl

campaign_avg_figb = pd.DataFrame()
campaign_avg_figb['t'] = t_bl/86400
campaign_avg_figb['gf'] = my_gf_bl

campaign_avg_stats = pd.DataFrame({'r squared': [my_r2_bl], 'mean age': [mean_age_bl], 'mode age': [mode_age_bl]})

campaign_avg_figa.to_pickle('./campaign_avg_figa.pkl')
campaign_avg_figb.to_pickle('./campaign_avg_figb.pkl')
campaign_avg_stats.to_pickle('./campaign_avg_stats.pkl')


# --------------- ver 2: BL TROPO
tau_tr = ratios_sort['TROPO_tau'].values

# get inputs
t_tr, exp_decay_matrix_tr, LT_tr = tts_mod.prep_for_tts(tau_tr)
# get tts 
my_mustar_tr, my_r2_tr, my_gf_tr, my_t_tr, mean_age_tr, mode_age_tr, best_k_tr = tts_mod.get_tts(utbl, tau_tr, t_tr, exp_decay_matrix_tr, LT_tr)

# --------------- ver 2: BL UT
tau_ut = ratios_sort['UT_tau'].values

# get inputs
t_ut, exp_decay_matrix_ut, LT_ut = tts_mod.prep_for_tts(tau_ut)
# get tts 
my_mustar_ut, my_r2_ut, my_gf_ut, my_t_ut, mean_age_ut, mode_age_ut, best_k_tr = tts_mod.get_tts(utbl, tau_ut, t_ut, exp_decay_matrix_ut, LT_ut)

############################ PLOT TTS OUTPUTS FOR EA. CASE ############################
# import my TTS module, need to add path to folder
import imp
imp.reload(tts_mod)

# --------------- start plot with BL case
title_str = r'$\tau_{BL}$: '
my_color = 'k'
overplot = 0
add_scatter = 1
add_r2 = 1 
add_meanmode = 1
# first plot only, dummies (will get real after first run creates fig)
width = 0
height = 0
my_ax = 0

fig, my_ax, width, height = tts_mod.plot_tts(tau_bl, my_mustar_bl, utbl, my_r2_bl, my_gf_bl, 
                                        my_t_bl, mean_age_bl, mode_age_bl, 
                                        my_color, overplot, add_scatter, add_r2, 
                                        add_meanmode, my_ax, width, height, title_str)

# --------------- add TROPO case 
title_str = r'$\tau_{tropo}$: '
my_color = [0.83, 0.13, 0.18]
overplot = 1
add_scatter = 1
add_r2 = 1 
add_meanmode = 1

tts_mod.plot_tts(tau_tr, my_mustar_tr, utbl, my_r2_tr, my_gf_tr, 
                                        my_t_tr, mean_age_tr, mode_age_tr, 
                                        my_color, overplot, add_scatter, add_r2, 
                                        add_meanmode, my_ax, width, height, title_str)

# --------------- add UT case 
title_str = r'$\tau_{UT}$: '
my_color = [0, 0.09, 0.66] #pantone blue
overplot = 2
add_scatter = 1
add_r2 = 1 
add_meanmode = 1

tts_mod.plot_tts(tau_ut, my_mustar_ut, utbl, my_r2_ut, my_gf_ut, 
                                        my_t_ut, mean_age_ut, mode_age_ut, 
                                        my_color, overplot, add_scatter, add_r2, 
                                        add_meanmode, my_ax, width, height, title_str)

# --------------- save figure 
svpath = '/UTLS/schelpon/TTS_2020/get_tts/figures/'
fig.savefig(svpath + 'tts_vary_tau.pdf')  
fig.savefig(svpath + 'tts_vary_tau.png')  
#fig.savefig(svpath + 'tts_vary_tau.svg')  



