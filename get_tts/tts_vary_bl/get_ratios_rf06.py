# script to calculate ratios for use in TTS method 
# match rf 06 to varying BL for ratios 
# 1) RF06 BL before anthropogenic from 
# 2) RF06 BL after anthropogenic from 
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
awas_df_rf06 = awas_df[awas_df['Flight'] == 'RF06']
awas_df_rf06_bl = awas_df_rf06[awas_df['GGALT'] < 2000]
awas_df_rf06_bl

toga_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/toga_data_df.pkl")
toga_df_rf06 = toga_df[toga_df['Flight'] == 'RF06']
toga_df_rf06_bl = toga_df_rf06[toga_df['GGALT'] < 2000]
toga_df_rf06_bl


################# -------------------- TOGA - FIND FRONT -------------------- #################
fig, ax = plt.subplots(figsize=(12,5), ncols = 2)
#
shear = toga_df_rf06_bl[(toga_df_rf06_bl['GGLAT']>15)]
south = toga_df_rf06_bl[toga_df_rf06_bl['GGLAT']<15]
ax[0].scatter(shear['GGLAT'], shear['Benzene'], c = 'r')
ax[0].scatter(south['GGLAT'], south['Benzene'], c = 'g')

#
s = ax[1].scatter(toga_df_rf06_bl['GGLON'], toga_df_rf06_bl['GGLAT'], c = toga_df_rf06_bl['Benzene'])
cbar = fig.colorbar(s)

# use 16.5 - 18 N as the front 
# use south of 16.5 as before the front

################# -------------------- TOGA  -------------------- #################
# get mean in UT and BL for 1) flights in total and 2) individual flights 
toga_means = pd.DataFrame()

# rf08
toga_means['UT - RF06'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF06')].mean()

# in shear 
toga_means['BL - In Shear'] = shear.mean()

# south of shear 
toga_means['BL - S of Shear'] = south.mean()

toga_means = toga_means.drop('GGALT').drop('GGLAT').drop('GGLON')
#toga_means.index.name = "Trace_Gas"
toga_means = toga_means.reset_index()
toga_means = toga_means.rename(columns={'index': 'Trace_Gas'})
toga_means

# ratios for 1) flights in total and 2) individual flights 
toga_ratios = pd.DataFrame()

toga_ratios['Trace_Gas'] = toga_means['Trace_Gas']
toga_ratios['RF06_In Shear'] = toga_means['UT - RF06']/toga_means['BL - In Shear']
toga_ratios['RF06_S of Shear'] = toga_means['UT - RF06']/toga_means['BL - S of Shear']
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
toga_ratios_full


###############################################################################################
################# -------------------- AWAS - FIND FRONT -------------------- #################
fig, ax = plt.subplots(figsize=(12,5), ncols = 2)

# divide at 15 N
shear = awas_df_rf06_bl[(awas_df_rf06['GGLAT']>15)]
south = awas_df_rf06_bl[(awas_df_rf06['GGLAT']<15)]
ax[0].scatter(shear['GGLAT'], shear['C6H6_Benzene'], c = 'r')
ax[0].scatter(south['GGLAT'], south['C6H6_Benzene'], c = 'g')

#
s = ax[1].scatter(awas_df_rf06_bl['GGLON'], awas_df_rf06_bl['GGLAT'], c = awas_df_rf06_bl['C6H6_Benzene'])
cbar = fig.colorbar(s)

################# -------------------- AWAS -------------------- #################
# get mean in UT and BL for 1) flights in total and 2) individual flights 
awas_means = pd.DataFrame()

# rf08
awas_means['UT - RF06'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF06')].mean()

# in shear 
awas_means['BL - In Shear'] = shear.mean()

# south of shear 
awas_means['BL - S of Shear'] = south.mean()

awas_means = awas_means.drop('GGALT').drop('GGLAT').drop('GGLON')
#toga_means.index.name = "Trace_Gas"
awas_means = awas_means.reset_index()
awas_means = awas_means.rename(columns={'index': 'Trace_Gas'})

# ratios for 1) flights in total and 2) individual flights 
awas_ratios = pd.DataFrame()

awas_ratios['Trace_Gas'] = awas_means['Trace_Gas']
awas_ratios['RF06_In Shear'] = awas_means['UT - RF06']/awas_means['BL - In Shear']
awas_ratios['RF06_S of Shear'] = awas_means['UT - RF06']/awas_means['BL - S of Shear']

# drop species names so doesnt duplicate column when merged 
awas_ratios = awas_ratios.drop('Trace_Gas', axis = 1)
awas_ratios

### add attribute to each species (BL, tropo, and UT lifetimes)
# read in from xls file to make dataframe
mypath2 = '/UTLS/schelpon/TTS_2020/contrast_readin/awas/awas_lifetimes_12162019.xlsx'
awas_lifetimes = pd.read_excel(mypath2)
len(awas_lifetimes)

# merge lifetimes to ratios 
awas_ratios_full = awas_lifetimes.merge(awas_ratios, left_index=True, right_index=True)
awas_ratios_full.insert(0, 'Instrument', 'AWAS')
awas_ratios_full

############################################################################################
################# -------------------- MERGE THE TWO  -------------------- #################
master_list = awas_ratios_full
master_list = master_list.append(toga_ratios_full, ignore_index = True, sort = None)

# pickle this!! 
master_list.to_pickle("./contrast_ratios_rf06.pkl")

# look at output 
master_list

