# script to calculate ratios for use in TTS method 
# match rf 08 to varying BL for ratios 
# 1) RF08 UT to RF08 BL 
# 2) RF08 UT to campaign average BL 
# 3) RF08 UT to RF06, 07, 08 BL 
# author: sofia chelpon
# date created: 2-17-2020
import numpy as np 
import xarray as xr
import pandas as pd 
import datetime 
import seaborn as sns
import datetime as dt
from scipy.optimize import least_squares

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits import mplot3d

# load in both toga and awas data pickles 
awas_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/awas_data_df.pkl")
toga_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/toga_data_df.pkl")

################# -------------------- TOGA  -------------------- #################
# get mean in UT and BL for 1) flights in total and 2) individual flights 
toga_means = pd.DataFrame()

# rf08
toga_means['UT - RF08'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF08')].mean()
toga_means['BL - RF08'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF08')].mean()

# all rf 
toga_means['BL - All RF'] = toga_df.loc[(toga_df['GGALT'] < 2000)].mean()

#nine days prior (RF 06, 07, 08)
nineday_flts = toga_df[toga_df['Flight'].isin(['RF06', 'RF07', 'RF08'])]
nineday_flts = nineday_flts[nineday_flts['GGALT'] < 2000]
toga_means['BL - 9days'] = nineday_flts.mean()

toga_means = toga_means.drop('GGALT').drop('GGLAT').drop('GGLON')
#toga_means.index.name = "Trace_Gas"
toga_means = toga_means.reset_index()
toga_means = toga_means.rename(columns={'index': 'Trace_Gas'})

# ratios for 1) flights in total and 2) individual flights 
toga_ratios = pd.DataFrame()

toga_ratios['Trace_Gas'] = toga_means['Trace_Gas']
toga_ratios['RF08_CampAvg'] = toga_means['UT - RF08']/toga_means['BL - All RF']
toga_ratios['RF08_RF08'] = toga_means['UT - RF08']/toga_means['BL - RF08']
toga_ratios['RF08_9days'] = toga_means['UT - RF08']/toga_means['BL - 9days']
toga_ratios

# drop species names so doesnt duplicate column when merged 
toga_ratios = toga_ratios.drop('Trace_Gas', axis = 1)

### add attribute to each species (BL, tropo, and UT lifetimes)
# read in from xls file to make dataframe
mypath2 = '/UTLS/schelpon/TTS_2020/contrast_readin/toga_lodhalf/toga_lifetimes_12162019.xlsx'
toga_lifetimes = pd.read_excel(mypath2)

# merge lifetimes to ratios
toga_ratios_full = toga_lifetimes.merge(toga_ratios, left_index=True, right_index=True)
toga_ratios_full.insert(0, 'Instrument', 'TOGA')

################# -------------------- AWAS  -------------------- #################
# get mean in UT and BL for 1) flights in total and 2) individual flights 
awas_means = pd.DataFrame()

# rf08
awas_means['UT - RF08'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF08')].mean()
awas_means['BL - RF08'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF08')].mean()

# all rf 
awas_means['BL - All RF'] = awas_df.loc[(awas_df['GGALT'] < 2000)].mean()

# nine days prior (RF 06, 07, 08)
del nineday_flts
nineday_flts = awas_df[awas_df['Flight'].isin(['RF06', 'RF07', 'RF08'])]
nineday_flts = nineday_flts[nineday_flts['GGALT'] < 2000]
awas_means['BL - 9days'] = nineday_flts.mean()

awas_means = awas_means.drop('GGALT').drop('GGLAT').drop('GGLON')
#toga_means.index.name = "Trace_Gas"
awas_means = awas_means.reset_index()
awas_means = awas_means.rename(columns={'index': 'Trace_Gas'})

# ratios for 1) flights in total and 2) individual flights 
awas_ratios = pd.DataFrame()

awas_ratios['Trace_Gas'] = awas_means['Trace_Gas']
awas_ratios['RF08_CampAvg'] = awas_means['UT - RF08']/awas_means['BL - All RF']
awas_ratios['RF08_RF08'] = awas_means['UT - RF08']/awas_means['BL - RF08']
awas_ratios['RF08_9days'] = awas_means['UT - RF08']/awas_means['BL - 9days']

# drop species names so doesnt duplicate column when merged 
awas_ratios = awas_ratios.drop('Trace_Gas', axis = 1)

### add attribute to each species (BL, tropo, and UT lifetimes)
# read in from xls file to make dataframe
mypath2 = '/UTLS/schelpon/TTS_2020/contrast_readin/awas/awas_lifetimes_12162019.xlsx'
awas_lifetimes = pd.read_excel(mypath2)
len(awas_lifetimes)

# merge lifetimes to ratios 
awas_ratios_full = awas_lifetimes.merge(awas_ratios, left_index=True, right_index=True)
awas_ratios_full.insert(0, 'Instrument', 'AWAS')

awas_ratios_full

################# -------------------- MERGE THE TWO  -------------------- #################
master_list = awas_ratios_full
master_list = master_list.append(toga_ratios_full, ignore_index = True, sort = None)

# pickle this!! 
master_list.to_pickle("./contrast_ratios_rf08.pkl")

# look at output 
master_list

