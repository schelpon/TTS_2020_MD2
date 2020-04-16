# get ratios for segment analysis 
# use BL of whole campaign 
# date created: 3/2/2020
# author: sofia chelpon 
import numpy as np 
import xarray as xr
import pandas as pd 
import datetime 
import seaborn as sns

import datetime as dt 

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits import mplot3d

#### ------------------- LOAD IN 
# data overall 
awas_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/awas_data_df_twp.pkl")
toga_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/toga_data_df_twp.pkl")

# segment data
awas_segments = pd.read_pickle("./awas_segments_twp.pkl")
awas_segments = awas_segments.drop(columns = 'GGALT').drop(columns = 'GGLAT').drop(columns ='GGLON').drop(columns = 'Notes')
# segment data 
toga_segments = pd.read_pickle("./toga_segments_twp.pkl")
toga_segments = toga_segments.drop(columns = 'GGALT').drop(columns = 'GGLAT').drop(columns ='GGLON')

##### --------------------- get campaign average BL means 
# AWAS 
awas_bl = pd.Series()
awas_bl = awas_df.loc[(awas_df['GGALT'] < 2000)].mean()
awas_bl = awas_bl.drop('GGALT').drop('GGLAT').drop('GGLON')
awas_bl.index.name = "Trace_Gas"

# TOGA
toga_bl = pd.Series()
toga_bl = toga_df.loc[(toga_df['GGALT'] < 2000)].mean()
toga_bl = toga_bl.drop('GGALT').drop('GGLAT').drop('GGLON')
toga_bl.index.name = "Trace_Gas"

######## ------------- GET AWAS RATIOS 
# thing to fill with ratios 
awas_seg_ratios = pd.DataFrame()
for col in awas_df.columns: 
    awas_seg_ratios[col] = ''
awas_seg_ratios = awas_seg_ratios.drop(columns = 'GGALT').drop(columns = 'GGLAT').drop(columns = 'GGLON').drop(columns = 'Notes').drop(columns = 'Intrument')
    
# loop through every segment and get ratio for it 
for idx in (np.arange(0, len(awas_segments))):
    # find segment, get info 
    awas_ut = awas_segments.iloc[idx]
    idx_info = pd.Series({'Time_UTC': awas_ut['Time_UTC'], 'Flight': awas_ut['Flight']})
    # get ratio 
    awas_ut = awas_ut.drop('Time_UTC').drop('Intrument').drop('Flight')
    idx_rat = awas_ut/awas_bl
    # merge to info 
    to_append = idx_info.append(idx_rat)
    to_append = pd.DataFrame(to_append).transpose()
    # append
    awas_seg_ratios = awas_seg_ratios.append(to_append, ignore_index = True)

######## ------------- GET TOGA RATIOS 
# thing to fill with ratios 
toga_seg_ratios = pd.DataFrame()
for col in toga_df.columns: 
    toga_seg_ratios[col] = ''
toga_seg_ratios = toga_seg_ratios.drop(columns = 'GGALT').drop(columns = 'GGLAT').drop(columns = 'GGLON').drop(columns = 'Notes').drop(columns = 'Intrument')
    
# loop through every segment and get ratio for it 
for idx in (np.arange(0, len(toga_segments))):
    # find segment, get info 
    toga_ut = toga_segments.iloc[idx]
    idx_info = pd.Series({'Time_UTC': toga_ut['Time_UTC'], 'Flight': toga_ut['Flight']})
    # get ratio 
    toga_ut = toga_ut.drop('Time_UTC').drop('Intrument').drop('Flight')
    idx_rat = toga_ut/toga_bl
    # merge to info 
    to_append = idx_info.append(idx_rat)
    to_append = pd.DataFrame(to_append).transpose()
    # append
    toga_seg_ratios = toga_seg_ratios.append(to_append, ignore_index = True)

### add attribute to each species (BL, tropo, and UT lifetimes)
fill = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan]], columns=['Trace_Gas', 'BL_tau', 'TROPO_tau', 'UT_tau'])
fill = fill.append(fill)

# --------- AWAS 
# read in from xls file to make dataframe - awas
mypath2 = '/UTLS/schelpon/TTS_2020/contrast_readin/awas/awas_lifetimes_12162019.xlsx'
awas_lifetimes = pd.read_excel(mypath2)
awas_lifetimes = fill.append(awas_lifetimes)
awas_lifetimes = awas_lifetimes.reset_index().drop('index', axis = 1)

# --------- TOGA
# read in from xls file to make dataframe - toga 
mypath2 = '/UTLS/schelpon/TTS_2020/contrast_readin/toga_lodhalf/toga_lifetimes_12162019.xlsx'
toga_lifetimes = pd.read_excel(mypath2)
toga_lifetimes = fill.append(toga_lifetimes)
toga_lifetimes = toga_lifetimes.reset_index().drop('index', axis = 1)


# In[10]:


# combine data from both instruments to one dataframe 
# --------- AWAS 
awas_seg_ratios = awas_seg_ratios.transpose()
awas_seg_ratios.insert(0, 'Instrument', 'AWAS')

# add lifetimes 
awas_seg_ratios.insert(1, 'BL_tau', awas_lifetimes['BL_tau'].values)
awas_seg_ratios.insert(2, 'TROPO_tau', awas_lifetimes['TROPO_tau'].values)
awas_seg_ratios.insert(3, 'UT_tau', awas_lifetimes['UT_tau'].values)

# --------- TOGA 
toga_seg_ratios = toga_seg_ratios.transpose()
toga_seg_ratios.insert(0, 'Instrument', 'TOGA')

# add lifetimes 
toga_seg_ratios.insert(1, 'BL_tau', toga_lifetimes['BL_tau'].values)
toga_seg_ratios.insert(2, 'TROPO_tau', toga_lifetimes['TROPO_tau'].values)
toga_seg_ratios.insert(3, 'UT_tau', toga_lifetimes['UT_tau'].values)


# In[12]:


# combine data from both instruments to one dataframe 
toga_seg_ratios = toga_seg_ratios.drop('Time_UTC', axis = 0)
toga_seg_ratios = toga_seg_ratios.drop('Flight', axis = 0)

ratios_comb = awas_seg_ratios.append(toga_seg_ratios)
ratios_comb


# pickle this!! 
ratios_comb.to_pickle("./contrast_ratios_ut_seg_twp.pkl")


#################################################################3
# save tracer names 
#### BL TAU -----------------------------------------------
ratios_sort_bl = ratios_comb
ratios_sort_bl = ratios_sort_bl.drop('Time_UTC').drop('Flight')
ratios_sort_bl = ratios_sort_bl.sort_values(['BL_tau'])

# save ordered bl tau as a variable 
tau_bl = ratios_sort_bl['BL_tau']

# drop uncecessary columns 
ratios_sort_bl = ratios_sort_bl.drop(columns = ['Instrument', 'BL_tau', 'TROPO_tau', 'UT_tau'])

# make a thing to fill with tracer names 
trcnames_allseg_bltau = pd.DataFrame()
for col in ratios_sort_bl.columns: 
    trcnames_allseg_bltau[col] = ''
trcnames_allseg_bltau

# loop through each segment 
col = list(ratios_sort_bl)
for i in col:
    utbl_full = np.array(ratios_sort_bl[i].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    tracer_names = ratios_sort_bl.index[utbl_not_null_idx]
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_utbl = np.append(my_utbl, filla)
        tracer_names = np.append(tracer_names, filla)
    else: 
        tracer_names = tracer_names.values 
        #tracer_names = np.ones([52])
        #tracer_names[:] = np.NaN
    # ----- save outputs of tracer names 
    trcnames_allseg_bltau[i] = tracer_names

trcnames_allseg_bltau.to_pickle("./trcnames_allseg_twp_bltau.pkl")


#### TROPO TAU -----------------------------------------------
ratios_sort_tr = ratios_comb
ratios_sort_tr = ratios_sort_tr.drop('Time_UTC').drop('Flight')
ratios_sort_tr = ratios_sort_tr.sort_values(['TROPO_tau'])

# save ordered bl tau as a variable 
tau_tr = ratios_sort_tr['TROPO_tau']

# drop uncecessary columns 
ratios_sort_tr = ratios_sort_tr.drop(columns = ['Instrument', 'BL_tau', 'TROPO_tau', 'UT_tau'])

# make a thing to fill with tracer names 
trcnames_allseg_trtau = pd.DataFrame()
for col in ratios_sort_tr.columns: 
    trcnames_allseg_trtau[col] = ''
trcnames_allseg_trtau

# loop through each segment 
col = list(ratios_sort_tr)
for i in col:
    utbl_full = np.array(ratios_sort_tr[i].values, dtype=np.float64)
    utbl_not_null_idx = np.argwhere(~np.isnan(utbl_full))
    # ----- inputs without nans 
    my_utbl = utbl_full[utbl_not_null_idx]
    tracer_names = ratios_sort_tr.index[utbl_not_null_idx]
    # ----- fill to make mu*, tau all length 52
    diffa = len(utbl_full) - len(my_utbl)
    if (diffa > 0):
        filla = np.empty((1,diffa))
        filla.fill(np.nan)
        my_utbl = np.append(my_utbl, filla)
        tracer_names = np.append(tracer_names, filla)
    else: 
        tracer_names = tracer_names.values 
        #tracer_names = np.ones([52])
        #tracer_names[:] = np.NaN
    # ----- save outputs of tracer names 
    trcnames_allseg_trtau[i] = tracer_names

trcnames_allseg_trtau.to_pickle("./trcnames_allseg_twp_trtau.pkl")


