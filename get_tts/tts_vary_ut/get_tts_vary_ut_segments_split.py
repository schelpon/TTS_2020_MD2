#!/usr/bin/env python
# coding: utf-8

# script to get TTS for all UT segments 
# date created: 3/2/2020
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
path = "/UTLS/schelpon/TTS_2020/get_tts/tts_vary_ut/data_prep/contrast_ratios_ut_seg.pkl"
contrast_ratios = pd.read_pickle(path)
info = contrast_ratios.iloc[[0, 1]]
segment_info = info.drop(columns = 'Instrument').drop(columns = 'BL_tau').drop(columns = 'TROPO_tau').drop(columns = 'UT_tau')
seg_info = segment_info.transpose()

# get index of each flight 
idx_rf05 = seg_info[seg_info['Flight'] == 'RF05'].index.tolist()
idx_rf06 = seg_info[seg_info['Flight'] == 'RF06'].index.tolist()
idx_rf07 = seg_info[seg_info['Flight'] == 'RF07'].index.tolist()
idx_rf08 = seg_info[seg_info['Flight'] == 'RF08'].index.tolist()
idx_rf09 = seg_info[seg_info['Flight'] == 'RF09'].index.tolist()
idx_rf10 = seg_info[seg_info['Flight'] == 'RF10'].index.tolist()
idx_rf11 = seg_info[seg_info['Flight'] == 'RF11'].index.tolist()
idx_rf12 = seg_info[seg_info['Flight'] == 'RF12'].index.tolist()
idx_rf13 = seg_info[seg_info['Flight'] == 'RF13'].index.tolist()
idx_rf14 = seg_info[seg_info['Flight'] == 'RF14'].index.tolist()

# sort 
ratios_sort = contrast_ratios
ratios_sort = ratios_sort.drop('Time_UTC').drop('Flight')
ratios_sort = ratios_sort.sort_values(['BL_tau'])

# save ordered bl tau as a variable 
tau = ratios_sort['BL_tau']

# drop uncecessary columns 
ratios_sort = ratios_sort.drop(columns = ['Instrument', 'BL_tau', 'TROPO_tau', 'UT_tau'])
ratios_sort.head()



###############################################################################################
################################ 		RF 05 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf05 = []
mean_rf05 = []
mode_rf05 =  []
num = []
bestk_rf05 = []

utbl_rf05 = pd.DataFrame()
mustar_rf05 = pd.DataFrame()
gf_rf05 = pd.DataFrame()
t_rf05 = pd.DataFrame()
tau_rf05 = pd.DataFrame()

for col in ratios_sort[idx_rf05].columns: 
    utbl_rf05[col] = ''
    mustar_rf05[col] = ''
    gf_rf05[col] = ''
    t_rf05[col] = ''
    tau_rf05[col] = ''

# lgnth of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf05]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf05.append(best_k)
    r2_rf05.append(my_r2)
    mean_rf05.append(mean_age)
    mode_rf05.append(mode_age)
    # ----- save to dataframes
    utbl_rf05[col] = np.ndarray.flatten(my_utbl)
    mustar_rf05[col] = np.ndarray.flatten(my_mustar)
    tau_rf05[col] = np.ndarray.flatten(my_tau)
    gf_rf05[col] = np.ndarray.flatten(my_gf)
    t_rf05[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf05 = seg_info[seg_info['Flight'] == 'RF05']

segment_info_rf05['r squared'] = r2_rf05
segment_info_rf05['mean age'] = mean_rf05
segment_info_rf05['mode age'] = mode_rf05
segment_info_rf05['best k'] = bestk_rf05

segment_info.to_pickle('./perflight_output/segment_info_rf05.pkl')

# save others 
utbl_rf05.to_pickle('./perflight_output/utbl_rf05.pkl')
mustar_rf05.to_pickle('./perflight_output/mustar_rf05.pkl')
tau_rf05.to_pickle('./perflight_output/tau_rf05.pkl')
gf_rf05.to_pickle('./perflight_output/gf_rf05.pkl')
t_rf05.to_pickle('./perflight_output/t_rf05.pkl')



#####################################################################################################
################################ 		RF 06 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf06 = []
mean_rf06 = []
mode_rf06 = []
num = []
bestk_rf06 = []

utbl_rf06 = pd.DataFrame()
mustar_rf06 = pd.DataFrame()
gf_rf06 = pd.DataFrame()
t_rf06 = pd.DataFrame()
tau_rf06 = pd.DataFrame()

for col in ratios_sort[idx_rf06].columns: 
    utbl_rf06[col] = ''
    mustar_rf06[col] = ''
    gf_rf06[col] = ''
    t_rf06[col] = ''
    tau_rf06[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf06]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf06.append(best_k)
    r2_rf06.append(my_r2)
    mean_rf06.append(mean_age)
    mode_rf06.append(mode_age)
    # ----- save to dataframes
    utbl_rf06[col] = np.ndarray.flatten(my_utbl)
    mustar_rf06[col] = np.ndarray.flatten(my_mustar)
    tau_rf06[col] = np.ndarray.flatten(my_tau)
    gf_rf06[col] = np.ndarray.flatten(my_gf)
    t_rf06[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf06 = seg_info[seg_info['Flight'] == 'RF06']

segment_info_rf06['r squared'] = r2_rf06
segment_info_rf06['mean age'] = mean_rf06
segment_info_rf06['mode age'] = mode_rf06
segment_info_rf06['best k'] = bestk_rf06

segment_info.to_pickle('./perflight_output/segment_info_rf06.pkl')

# save others 
utbl_rf06.to_pickle('./perflight_output/utbl_rf06.pkl')
mustar_rf06.to_pickle('./perflight_output/mustar_rf06.pkl')
tau_rf06.to_pickle('./perflight_output/tau_rf06.pkl')
gf_rf06.to_pickle('./perflight_output/gf_rf06.pkl')
t_rf06.to_pickle('./perflight_output/t_rf06.pkl')


#####################################################################################################
################################ 		RF 07 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf07 = []
mean_rf07 = []
mode_rf07 = []
num = []
bestk_rf07 = []

utbl_rf07 = pd.DataFrame()
mustar_rf07 = pd.DataFrame()
gf_rf07 = pd.DataFrame()
t_rf07 = pd.DataFrame()
tau_rf07 = pd.DataFrame()

for col in ratios_sort[idx_rf07].columns: 
    utbl_rf07[col] = ''
    mustar_rf07[col] = ''
    gf_rf07[col] = ''
    t_rf07[col] = ''
    tau_rf07[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf07]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf07.append(best_k)
    r2_rf07.append(my_r2)
    mean_rf07.append(mean_age)
    mode_rf07.append(mode_age)
    # ----- save to dataframes
    utbl_rf07[col] = np.ndarray.flatten(my_utbl)
    mustar_rf07[col] = np.ndarray.flatten(my_mustar)
    tau_rf07[col] = np.ndarray.flatten(my_tau)
    gf_rf07[col] = np.ndarray.flatten(my_gf)
    t_rf07[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf07 = seg_info[seg_info['Flight'] == 'RF07']

segment_info_rf07['r squared'] = r2_rf07
segment_info_rf07['mean age'] = mean_rf07
segment_info_rf07['mode age'] = mode_rf07
segment_info_rf07['best k'] = bestk_rf07

segment_info.to_pickle('./perflight_output/segment_info_rf07.pkl')

# save others 
utbl_rf07.to_pickle('./perflight_output/utbl_rf07.pkl')
mustar_rf07.to_pickle('./perflight_output/mustar_rf07.pkl')
tau_rf07.to_pickle('./perflight_output/tau_rf07.pkl')
gf_rf07.to_pickle('./perflight_output/gf_rf07.pkl')
t_rf07.to_pickle('./perflight_output/t_rf07.pkl')


#####################################################################################################
################################ 		RF 08 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf08 = []
mean_rf08 = []
mode_rf08 = []
num = []
bestk_rf08 = []

utbl_rf08 = pd.DataFrame()
mustar_rf08 = pd.DataFrame()
gf_rf08 = pd.DataFrame()
t_rf08 = pd.DataFrame()
tau_rf08 = pd.DataFrame()

for col in ratios_sort[idx_rf08].columns: 
    utbl_rf08[col] = ''
    mustar_rf08[col] = ''
    gf_rf08[col] = ''
    t_rf08[col] = ''
    tau_rf08[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf08]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf08.append(best_k)
    r2_rf08.append(my_r2)
    mean_rf08.append(mean_age)
    mode_rf08.append(mode_age)
    # ----- save to dataframes
    utbl_rf08[col] = np.ndarray.flatten(my_utbl)
    mustar_rf08[col] = np.ndarray.flatten(my_mustar)
    tau_rf08[col] = np.ndarray.flatten(my_tau)
    gf_rf08[col] = np.ndarray.flatten(my_gf)
    t_rf08[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf08 = seg_info[seg_info['Flight'] == 'RF08']

segment_info_rf08['r squared'] = r2_rf08
segment_info_rf08['mean age'] = mean_rf08
segment_info_rf08['mode age'] = mode_rf08
segment_info_rf08['best k'] = bestk_rf08

segment_info.to_pickle('./perflight_output/segment_info_rf08.pkl')

# save others 
utbl_rf08.to_pickle('./perflight_output/utbl_rf08.pkl')
mustar_rf08.to_pickle('./perflight_output/mustar_rf08.pkl')
tau_rf08.to_pickle('./perflight_output/tau_rf08.pkl')
gf_rf08.to_pickle('./perflight_output/gf_rf08.pkl')
t_rf08.to_pickle('./perflight_output/t_rf08.pkl')


#####################################################################################################
################################ 		RF 09 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf09 = []
mean_rf09 = []
mode_rf09 = []
num = []
bestk_rf09 = []

utbl_rf09 = pd.DataFrame()
mustar_rf09 = pd.DataFrame()
gf_rf09 = pd.DataFrame()
t_rf09 = pd.DataFrame()
tau_rf09 = pd.DataFrame()

for col in ratios_sort[idx_rf09].columns: 
    utbl_rf09[col] = ''
    mustar_rf09[col] = ''
    gf_rf09[col] = ''
    t_rf09[col] = ''
    tau_rf09[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf09]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf09.append(best_k)
    r2_rf09.append(my_r2)
    mean_rf09.append(mean_age)
    mode_rf09.append(mode_age)
    # ----- save to dataframes
    utbl_rf09[col] = np.ndarray.flatten(my_utbl)
    mustar_rf09[col] = np.ndarray.flatten(my_mustar)
    tau_rf09[col] = np.ndarray.flatten(my_tau)
    gf_rf09[col] = np.ndarray.flatten(my_gf)
    t_rf09[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf09 = seg_info[seg_info['Flight'] == 'RF09']

segment_info_rf09['r squared'] = r2_rf09
segment_info_rf09['mean age'] = mean_rf09
segment_info_rf09['mode age'] = mode_rf09
segment_info_rf09['best k'] = bestk_rf09

segment_info.to_pickle('./perflight_output/segment_info_rf09.pkl')

# save others 
utbl_rf09.to_pickle('./perflight_output/utbl_rf09.pkl')
mustar_rf09.to_pickle('./perflight_output/mustar_rf09.pkl')
tau_rf09.to_pickle('./perflight_output/tau_rf09.pkl')
gf_rf09.to_pickle('./perflight_output/gf_rf09.pkl')
t_rf09.to_pickle('./perflight_output/t_rf09.pkl')



#####################################################################################################
################################ 		RF 10 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf10 = []
mean_rf10 = []
mode_rf10 = []
num = []
bestk_rf10 = []

utbl_rf10 = pd.DataFrame()
mustar_rf10 = pd.DataFrame()
gf_rf10 = pd.DataFrame()
t_rf10 = pd.DataFrame()
tau_rf10 = pd.DataFrame()

for col in ratios_sort[idx_rf10].columns: 
    utbl_rf10[col] = ''
    mustar_rf10[col] = ''
    gf_rf10[col] = ''
    t_rf10[col] = ''
    tau_rf10[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf10]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf10.append(best_k)
    r2_rf10.append(my_r2)
    mean_rf10.append(mean_age)
    mode_rf10.append(mode_age)
    # ----- save to dataframes
    utbl_rf10[col] = np.ndarray.flatten(my_utbl)
    mustar_rf10[col] = np.ndarray.flatten(my_mustar)
    tau_rf10[col] = np.ndarray.flatten(my_tau)
    gf_rf10[col] = np.ndarray.flatten(my_gf)
    t_rf10[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf10 = seg_info[seg_info['Flight'] == 'RF10']

segment_info_rf10['r squared'] = r2_rf10
segment_info_rf10['mean age'] = mean_rf10
segment_info_rf10['mode age'] = mode_rf10
segment_info_rf10['best k'] = bestk_rf10

segment_info.to_pickle('./perflight_output/segment_info_rf10.pkl')

# save others 
utbl_rf10.to_pickle('./perflight_output/utbl_rf10.pkl')
mustar_rf10.to_pickle('./perflight_output/mustar_rf10.pkl')
tau_rf10.to_pickle('./perflight_output/tau_rf10.pkl')
gf_rf10.to_pickle('./perflight_output/gf_rf10.pkl')
t_rf10.to_pickle('./perflight_output/t_rf10.pkl')


#####################################################################################################
################################ 		RF 11 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf11 = []
mean_rf11 = []
mode_rf11 = []
num = []
bestk_rf11 = []

utbl_rf11 = pd.DataFrame()
mustar_rf11 = pd.DataFrame()
gf_rf11 = pd.DataFrame()
t_rf11 = pd.DataFrame()
tau_rf11 = pd.DataFrame()

for col in ratios_sort[idx_rf11].columns: 
    utbl_rf11[col] = ''
    mustar_rf11[col] = ''
    gf_rf11[col] = ''
    t_rf11[col] = ''
    tau_rf11[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf11]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf11.append(best_k)
    r2_rf11.append(my_r2)
    mean_rf11.append(mean_age)
    mode_rf11.append(mode_age)
    # ----- save to dataframes
    utbl_rf11[col] = np.ndarray.flatten(my_utbl)
    mustar_rf11[col] = np.ndarray.flatten(my_mustar)
    tau_rf11[col] = np.ndarray.flatten(my_tau)
    gf_rf11[col] = np.ndarray.flatten(my_gf)
    t_rf11[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf11 = seg_info[seg_info['Flight'] == 'RF11']

segment_info_rf11['r squared'] = r2_rf11
segment_info_rf11['mean age'] = mean_rf11
segment_info_rf11['mode age'] = mode_rf11
segment_info_rf11['best k'] = bestk_rf11

segment_info.to_pickle('./perflight_output/segment_info_rf11.pkl')

# save others 
utbl_rf11.to_pickle('./perflight_output/utbl_rf11.pkl')
mustar_rf11.to_pickle('./perflight_output/mustar_rf11.pkl')
tau_rf11.to_pickle('./perflight_output/tau_rf11.pkl')
gf_rf11.to_pickle('./perflight_output/gf_rf11.pkl')
t_rf11.to_pickle('./perflight_output/t_rf11.pkl')



#####################################################################################################
################################ 		RF 12 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf12 = []
mean_rf12 = []
mode_rf12 = []
num = []
bestk_rf12 = []

utbl_rf12 = pd.DataFrame()
mustar_rf12 = pd.DataFrame()
gf_rf12 = pd.DataFrame()
t_rf12 = pd.DataFrame()
tau_rf12 = pd.DataFrame()

for col in ratios_sort[idx_rf12].columns: 
    utbl_rf12[col] = ''
    mustar_rf12[col] = ''
    gf_rf12[col] = ''
    t_rf12[col] = ''
    tau_rf12[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf12]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf12.append(best_k)
    r2_rf12.append(my_r2)
    mean_rf12.append(mean_age)
    mode_rf12.append(mode_age)
    # ----- save to dataframes
    utbl_rf12[col] = np.ndarray.flatten(my_utbl)
    mustar_rf12[col] = np.ndarray.flatten(my_mustar)
    tau_rf12[col] = np.ndarray.flatten(my_tau)
    gf_rf12[col] = np.ndarray.flatten(my_gf)
    t_rf12[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf12 = seg_info[seg_info['Flight'] == 'RF12']

segment_info_rf12['r squared'] = r2_rf12
segment_info_rf12['mean age'] = mean_rf12
segment_info_rf12['mode age'] = mode_rf12
segment_info_rf12['best k'] = bestk_rf12

segment_info.to_pickle('./perflight_output/segment_info_rf12.pkl')

# save others 
utbl_rf12.to_pickle('./perflight_output/utbl_rf12.pkl')
mustar_rf12.to_pickle('./perflight_output/mustar_rf12.pkl')
tau_rf12.to_pickle('./perflight_output/tau_rf12.pkl')
gf_rf12.to_pickle('./perflight_output/gf_rf12.pkl')
t_rf12.to_pickle('./perflight_output/t_rf12.pkl')


#####################################################################################################
################################ 		RF 13 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf13 = []
mean_rf13 = []
mode_rf13 = []
num = []
bestk_rf13 = []

utbl_rf13 = pd.DataFrame()
mustar_rf13 = pd.DataFrame()
gf_rf13 = pd.DataFrame()
t_rf13 = pd.DataFrame()
tau_rf13 = pd.DataFrame()

for col in ratios_sort[idx_rf13].columns: 
    utbl_rf13[col] = ''
    mustar_rf13[col] = ''
    gf_rf13[col] = ''
    t_rf13[col] = ''
    tau_rf13[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf13]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf13.append(best_k)
    r2_rf13.append(my_r2)
    mean_rf13.append(mean_age)
    mode_rf13.append(mode_age)
    # ----- save to dataframes
    utbl_rf13[col] = np.ndarray.flatten(my_utbl)
    mustar_rf13[col] = np.ndarray.flatten(my_mustar)
    tau_rf13[col] = np.ndarray.flatten(my_tau)
    gf_rf13[col] = np.ndarray.flatten(my_gf)
    t_rf13[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf13 = seg_info[seg_info['Flight'] == 'RF13']

segment_info_rf13['r squared'] = r2_rf13
segment_info_rf13['mean age'] = mean_rf13
segment_info_rf13['mode age'] = mode_rf13
segment_info_rf13['best k'] = bestk_rf13

segment_info.to_pickle('./perflight_output/segment_info_rf13.pkl')

# save others 
utbl_rf13.to_pickle('./perflight_output/utbl_rf13.pkl')
mustar_rf13.to_pickle('./perflight_output/mustar_rf13.pkl')
tau_rf13.to_pickle('./perflight_output/tau_rf13.pkl')
gf_rf13.to_pickle('./perflight_output/gf_rf13.pkl')
t_rf13.to_pickle('./perflight_output/t_rf13.pkl')



#####################################################################################################
################################ 		RF 14 			#############################
############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# --------------- things to fill 
r2_rf14 = []
mean_rf14 = []
mode_rf14 = []
num = []
bestk_rf14 = []

utbl_rf14 = pd.DataFrame()
mustar_rf14 = pd.DataFrame()
gf_rf14 = pd.DataFrame()
t_rf14 = pd.DataFrame()
tau_rf14 = pd.DataFrame()

for col in ratios_sort[idx_rf14].columns: 
    utbl_rf14[col] = ''
    mustar_rf14[col] = ''
    gf_rf14[col] = ''
    t_rf14[col] = ''
    tau_rf14[col] = ''

# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort[idx_rf14]:
    print(col)
    # ----- remove nans or else tts function fails 
    utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    my_tau = tau[utbl_not_null_idx]
    #
    # ----- run tts function 
    t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
    my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
    #
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_tau = np.append(my_tau, filla)
        my_mustar = np.append(my_mustar, filla)
        my_utbl = np.append(my_utbl, filla)
    # ----- fill to make gf, t all length 275999
    diffb = 275999 - len(my_gf)
    if (diffb > 0):
        fillb = np.empty((1,diffb))
        fillb.fill(np.nan)
        my_gf = np.append(my_gf, fillb)
        my_t = np.append(my_t, fillb)
    #
    # ----- save individual values 
    bestk_rf14.append(best_k)
    r2_rf14.append(my_r2)
    mean_rf14.append(mean_age)
    mode_rf14.append(mode_age)
    # ----- save to dataframes
    utbl_rf14[col] = np.ndarray.flatten(my_utbl)
    mustar_rf14[col] = np.ndarray.flatten(my_mustar)
    tau_rf14[col] = np.ndarray.flatten(my_tau)
    gf_rf14[col] = np.ndarray.flatten(my_gf)
    t_rf14[col] = np.ndarray.flatten(my_t)

# -------------------- make dataframe for r2, mean, mode, segment info 
# save outputs
segment_info_rf14 = seg_info[seg_info['Flight'] == 'RF14']

segment_info_rf14['r squared'] = r2_rf14
segment_info_rf14['mean age'] = mean_rf14
segment_info_rf14['mode age'] = mode_rf14
segment_info_rf14['best k'] = bestk_rf14

segment_info.to_pickle('./perflight_output/segment_info_rf14.pkl')

# save others 
utbl_rf14.to_pickle('./perflight_output/utbl_rf14.pkl')
mustar_rf14.to_pickle('./perflight_output/mustar_rf14.pkl')
tau_rf14.to_pickle('./perflight_output/tau_rf14.pkl')
gf_rf14.to_pickle('./perflight_output/gf_rf14.pkl')
t_rf14.to_pickle('./perflight_output/t_rf14.pkl')











