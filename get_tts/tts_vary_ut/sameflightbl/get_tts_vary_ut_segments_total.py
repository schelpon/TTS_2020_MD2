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
path = "./contrast_ratios_ut_seg_sameflightbl.pkl"
contrast_ratios = pd.read_pickle(path)
info = contrast_ratios.iloc[[0, 1]]
segment_info = info.drop(columns = 'Instrument').drop(columns = 'BL_tau').drop(columns = 'TROPO_tau').drop(columns = 'UT_tau')

# sort 
ratios_sort = contrast_ratios
ratios_sort = ratios_sort.drop('Time_UTC').drop('Flight')
ratios_sort = ratios_sort.sort_values(['BL_tau'])

# save ordered bl tau as a variable 
tau = ratios_sort['BL_tau']

# drop uncecessary columns 
ratios_sort = ratios_sort.drop(columns = ['Instrument', 'BL_tau', 'TROPO_tau', 'UT_tau'])
ratios_sort

############################ GET TTS OUTPUTS FOR EA. CASE ############################
# --------------- test with a few seg 
# save outputs to plot later 
r2_allseg = []
mean_allseg = []
mode_allseg = []
bestk_allseg = []
num = []

utbl_allseg = pd.DataFrame()
mustar_allseg = pd.DataFrame()
gf_allseg = pd.DataFrame()
t_allseg = pd.DataFrame()
tau_allseg = pd.DataFrame()

for col in ratios_sort.columns: 
    utbl_allseg[col] = ''
    mustar_allseg[col] = ''
    gf_allseg[col] = ''
    t_allseg[col] = ''
    tau_allseg[col] = ''

############ --------------- LOOP THRU EACH SEGMENT, GET TTS OUTPUT --------------- ###########
# max length of G(t), usually 275999 but make higher so it doesnt fail 
topg = 276000

for col in ratios_sort:
	print(col)
	# ----- remove nans or else tts function fails 
	utbl_full = np.array(ratios_sort[col].values, dtype=np.float64)
	utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
	# ----- inputs without nans 
	my_utbl = utbl_full[utbl_not_null_idx]
	my_tau = tau[utbl_not_null_idx]
	# ----- run tts function 
	if (len(my_utbl) > 0):
		t, exp_decay_matrix, LT = tts_mod.prep_for_tts(my_tau)
		my_mustar, my_r2, my_gf, my_t, mean_age, mode_age, best_k = tts_mod.get_tts(my_utbl, my_tau, t, exp_decay_matrix, LT)
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
	if (len(my_utbl) == 0): 
		# mu - tau, mu* 
		my_utbl = np.empty((1,52))
		my_utbl[:] = np.NaN 
		my_tau = my_utbl
		my_mustar = my_utbl		
		# gf and time 
		my_gf = np.empty((275999,))
		my_gf[:] = np.NaN
		my_t = my_gf
		#individaul outputs 
		best_k = -999
		mode_age = -999
		mean_age = -999	
		my_r2 = -999
	# ----- save individual values 
	r2_allseg.append(my_r2)
	mean_allseg.append(mean_age)
	mode_allseg.append(mode_age)
	bestk_allseg.append(best_k)
	# ----- save to dataframes
	utbl_allseg[col] = np.ndarray.flatten(my_utbl)
	mustar_allseg[col] = np.ndarray.flatten(my_mustar)
	tau_allseg[col] = np.ndarray.flatten(my_tau)
	gf_allseg[col] = np.ndarray.flatten(my_gf)
	t_allseg[col] = np.ndarray.flatten(my_t)


############ --------------- SAVE OUTPUTS TO PICKLE --------------- ###########
# make dataframe for r2, mean, mode, segment info 
r2_allseg = pd.Series(r2_allseg)
mean_allseg = pd.Series(mean_allseg)
mode_allseg = pd.Series(mode_allseg)

segment_info = segment_info.transpose()

segment_info['r squared'] = r2_allseg
segment_info['mean age'] = mean_allseg
segment_info['mode age'] = mode_allseg

segment_info.to_pickle('./segment_info_sameflightbl.pkl')

# save others 
utbl_allseg.to_pickle('./utbl_allseg_sameflightbl.pkl')
mustar_allseg.to_pickle('./mustar_allseg_sameflightbl.pkl')
tau_allseg.to_pickle('./tau_allseg_sameflightbl.pkl')
gf_allseg.to_pickle('./gf_allseg_sameflightbl.pkl')
t_allseg.to_pickle('./t_allseg_sameflightbl.pkl')




