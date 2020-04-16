# script to plot TTS for all UT segments 
# date created: 3/3/2020
# author: sofia chelpon

############ --------------- PREP WORKSPACE --------------- ###########
import numpy as np 
import pandas as pd

import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns

# import my TTS module, need to add path to folder
import sys
sys.path.insert(1, '/UTLS/schelpon/TTS_2020/base_tts_code/')
import tts_mod

############ --------------- LOAD SEGMENT DATA --------------- ###########
utbl_allseg = pd.read_pickle('./utbl_allseg_campavgbl.pkl')
mustar_allseg = pd.read_pickle('./mustar_allseg_campavgbl.pkl')
tau_allseg = pd.read_pickle('./tau_allseg_campavgbl.pkl')
t_allseg = pd.read_pickle('./t_allseg_campavgbl.pkl')
gf_allseg = pd.read_pickle('./gf_allseg_campavgbl.pkl')
seg_info = pd.read_pickle('./segment_info_campavgbl.pkl')

############ --------------- LOAD CAMPAIGN AVERAGE DATA --------------- ###########
campaign_avg_figa = pd.read_pickle('/UTLS/schelpon/TTS_2020/get_tts/tts_vary_tau/campaign_avg_figa.pkl')
campaign_avg_figb = pd.read_pickle('/UTLS/schelpon/TTS_2020/get_tts/tts_vary_tau/campaign_avg_figb.pkl')
campaign_avg_stats = pd.read_pickle('/UTLS/schelpon/TTS_2020/get_tts/tts_vary_tau/campaign_avg_stats.pkl')

campav_tau = campaign_avg_figa['tau'].values
campav_mustar = campaign_avg_figa['mustar'].values
campav_utbl = campaign_avg_figa['utbl'].values
campav_r2 = campaign_avg_stats['r squared'].values
campav_r2 = campav_r2[0]
campav_gf = campaign_avg_figb['gf'].values
campav_t = campaign_avg_figb['t'].values
campav_mean_age = campaign_avg_stats['mean age'].values
campav_mean_age = campav_mean_age[0]
campav_mode_age = campaign_avg_stats['mode age'].values
campav_mode_age = campav_mode_age[0]


############ --------------- FILTER BY R^2 VALUES --------------- ###########
high_r2_idx = np.ndarray.flatten(np.argwhere(seg_info['r squared'] >= 0.65))

seg_info_screened = seg_info.iloc[high_r2_idx]

# screen vars 
mustar_allseg_screened = mustar_allseg[high_r2_idx]
utbl_allseg_screened = utbl_allseg[high_r2_idx]
tau_allseg_screened = tau_allseg[high_r2_idx]

gf_allseg_screened = gf_allseg[high_r2_idx]
t_allseg_screened = t_allseg[high_r2_idx]


############ --------------- FIND MIN/MAX CURVES --------------- ###########
min_mode_loc = np.argmin(seg_info_screened['mode age']) 
max_mode_loc = np.argmax(seg_info_screened['mode age']) 

min_mean_age = np.min(seg_info_screened['mean age']) 
max_mean_age = np.max(seg_info_screened['mean age']) 
print(min_mean_age, max_mean_age)

min_mode_age = np.min(seg_info_screened['mode age']) 
max_mode_age = np.max(seg_info_screened['mode age']) 
print(min_mode_age, max_mode_age)

# utbl  
min_utbl = utbl_allseg_screened[min_mode_loc].values
max_utbl = utbl_allseg_screened[max_mode_loc].values

min_r2 = np.min(seg_info_screened['r squared']) 
max_r2 = np.max(seg_info_screened['r squared']) 

min_mustar = mustar_allseg_screened[min_mode_loc].values
max_mustar = mustar_allseg_screened[max_mode_loc].values

min_tau = tau_allseg_screened[min_mode_loc].values
max_tau = tau_allseg_screened[max_mode_loc].values

min_gf = gf_allseg_screened[min_mode_loc].values
max_gf = gf_allseg_screened[max_mode_loc].values

min_t = t_allseg_screened[min_mode_loc].values
max_t = t_allseg_screened[max_mode_loc].values


###########################################################################################
###########################################################################################
###########################################################################################


############ --------------- PLOT IT! --------------- ###########
add_meanmode = 0
add_scatter = 0
add_r2 = 0

for idx in np.arange(0, (len(gf_allseg_screened.columns))):
	# pull that column 
	my_r2 = seg_info_screened['r squared'].iloc[idx]
        mean_age = seg_info_screened['mean age'].iloc[idx]
        mode_age = seg_info_screened['mode age'].iloc[idx]
        #
        my_tau = tau_allseg_screened.iloc[:,idx].values
        my_mustar = mustar_allseg_screened.iloc[:,idx].values
        my_utbl = utbl_allseg_screened.iloc[:,idx].values
        #
        my_gf = gf_allseg_screened.iloc[:,idx].values
        my_t = t_allseg_screened.iloc[:,idx].values
        # plotting factors 
        title_str = ' '
        my_color = [0.70, 0.75, 0.71] #ash gray    add_scatter = 0
        add_r2 = 0
        add_meanmode = 0
        #plot 
        if (idx == 0):
   	     overplot = 0
       	     width = 0
	     height = 0
             my_ax = 0
             fig, my_ax, width, height = tts_mod.plot_tts(my_tau, my_mustar, my_utbl, my_r2, 
                                             my_gf, my_t, mean_age, mode_age, 
                                             my_color, overplot, add_scatter, add_r2, add_meanmode, 
                                             my_ax, width, height, title_str)
        else: 
        	overplot = 1
	        tts_mod.plot_tts(my_tau, my_mustar, my_utbl, my_r2, 
                                             my_gf, my_t, mean_age, mode_age, 
                                             my_color, overplot, add_scatter, add_r2, add_meanmode, 
                                             my_ax, width, height, title_str)
# add extremes with scatter and r^2 
add_meanmode = 1 
add_scatter = 1
add_r2 = 1 

# colors
myred = [0.83, 0.13, 0.18] 
myblue = [0, 0.09, 0.66]

# minimum 
overplot = 1
add_meanmode = 1 
add_scatter = 1
add_r2 = 1 
title_str = 'Minimum Mode: '
my_color = myred
tts_mod.plot_tts(min_tau, min_mustar, min_utbl, min_r2, 
                        min_gf, min_t, min_mean_age, min_mode_age, 
                        my_color, overplot, add_scatter, add_r2, add_meanmode, 
                        my_ax, width, height, title_str)

# campaign average
overplot = 2
add_meanmode = 1 
add_scatter = 0
add_r2 = 1 
title_str = 'Campaign Average: '
my_color = 'k'
tts_mod.plot_tts(campav_tau, campav_mustar, campav_utbl, campav_r2, 
                        campav_gf, campav_t, campav_mean_age, campav_mode_age, 
                        my_color, overplot, add_scatter, add_r2, add_meanmode, 
                        my_ax, width, height, title_str)
# maximum 
overplot = 3
add_meanmode = 1 
add_scatter = 1
add_r2 = 1 
title_str = 'Maximum Mode: '
my_color = myblue
tts_mod.plot_tts(max_tau, max_mustar, max_utbl, max_r2, 
                        max_gf, min_t, max_mean_age, max_mode_age, 
                        my_color, overplot, add_scatter, add_r2, add_meanmode, 
                        my_ax, width, height, title_str)

# add grid
ax0, ax1 = my_ax
ax0.grid(which = 'major')
ax1.grid(which = 'major')

# --------------- save figure 
svpath = '/UTLS/schelpon/TTS_2020/get_tts/figures/'
fig.savefig(svpath + 'tts_vary_ut_campavgbl.png')  


###########################################################################################
###########################################################################################
###########################################################################################
############ --------------- MEAN, MODE BOXPLOTS --------------- ###########
# isolate mean and mode 
seg_info_clip = pd.DataFrame()
seg_info_clip['Mean Age'] = seg_info_screened['mean age'].values
seg_info_clip['Mode Age'] = seg_info_screened['mode age'].values

# plot 
mygray = [0.70, 0.75, 0.71]

fig, ax = plt.subplots(figsize=(10, 6), ncols=1)
sns.set(font_scale=1)
ax = sns.boxplot(data = seg_info_clip, linewidth = 2, orient = 'h', color = mygray)
#ax.grid(which = 'major')
sns.set_style("whitegrid")
ax.set_title('c) Distribution of Mean and Modal Transit Times', fontsize = 20)
ax.set_xlabel("Transit Time [days]" ,fontsize=15)
ax.tick_params(labelsize=15)

# --------------- save figure 
svpath = '/UTLS/schelpon/TTS_2020/get_tts/figures/'
fig.savefig(svpath + 'boxplot_vary_ut_campavgbl.png')  

###########################################################################################
###########################################################################################
###########################################################################################
############ --------------- MEAN, MODE BOXPLOTS PER RF --------------- ###########
# isolate mean and mode 
means_perrf = pd.DataFrame()
means_perrf['Mean Age'] = seg_info_screened['mean age'].values
means_perrf['Research Flight'] = seg_info_screened['Flight'].values
seg_avg_mean = means_perrf['Mean Age'].mean()
print(seg_avg_mean)

modes_perrf = pd.DataFrame()
modes_perrf['Research Flight'] = seg_info_screened['Flight'].values
modes_perrf['Mode Age'] = seg_info_screened['mode age'].values
seg_avg_mode = modes_perrf['Mode Age'].mean()
print(seg_avg_mode)

# plot - MEANS 
sns.set(font_scale=2)
sns.set_style("whitegrid")

g = sns.catplot(x = 'Research Flight', y = 'Mean Age', data = means_perrf,                 kind = 'box', color = mygray, height=7, aspect=3, linewidth = 3)

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('b) Distrubution of Mean Transit Times',  fontsize = 30)

plt.plot([-1, 10], [seg_avg_mean, seg_avg_mean], linewidth = 5, color = myred)
plt.plot([-1, 10], [campav_mean_age, campav_mean_age], linewidth = 5, color = myblue)

plt.text(8, 28, 'Campaign Average', color = myblue, fontsize = 26)
plt.text(8, 26, 'Segment Average', color = myred, fontsize = 26)

plt.xlim([-1, 10])
plt.ylim([0, 30])

# counts 
nobs = means_perrf['Research Flight'].value_counts().values
nobs = [str(x) for x in nobs.tolist()]
nobs = ["n: " + i for i in nobs]

# Add it to the plot
for idx, nn in enumerate(nobs):
    plt.text(idx, 0.5, nn, horizontalalignment='center',  
             fontsize=20, color='k', weight='bold')

# --------------- save figure 
svpath = '/UTLS/schelpon/TTS_2020/get_tts/figures/'
g.savefig(svpath + 'boxplot_vary_ut_means_campavgbl.png')  

###########################################################################################
# plot - MODES
sns.set(font_scale=2)
sns.set_style("whitegrid")

mygray = [0.70, 0.75, 0.71]
myred = [0.83, 0.13, 0.18] 
myblue = [0, 0.09, 0.66]

h = sns.catplot(x = 'Research Flight', y = 'Mode Age', data = modes_perrf,                 kind = 'box', color = mygray, height=7, aspect=3, linewidth = 3)

h.fig.subplots_adjust(top=0.9)
h.fig.suptitle('b) Distrubution of Modal Transit Times',  fontsize = 30)

plt.plot([-1, 10], [seg_avg_mode, seg_avg_mode], linewidth = 5, color = myred)
plt.plot([-1, 10], [campav_mode_age, campav_mode_age], linewidth = 5, color = myblue)

plt.text(8, 7.5, 'Campaign Average', color = myblue, fontsize = 26)
plt.text(8, 7, 'Segment Average', color = myred, fontsize = 26)

plt.xlim([-1, 10])
plt.ylim([0, 8])

# counts 
nobs = modes_perrf['Research Flight'].value_counts().values
nobs = [str(x) for x in nobs.tolist()]
nobs = ["n: " + i for i in nobs]

# Add it to the plot
for idx, nn in enumerate(nobs):
    plt.text(idx, 0.1, nn, horizontalalignment='center',  
             fontsize=20, color='k', weight='bold')

# --------------- save figure 
svpath = '/UTLS/schelpon/TTS_2020/get_tts/figures/'
h.savefig(svpath + 'boxplot_vary_ut_modes_campavgbl.png')  


