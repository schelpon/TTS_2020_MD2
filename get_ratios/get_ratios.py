#!/usr/bin/env python
# coding: utf-8

# script to calculate ratios for use in TTS method 
# author: sofia chelpon
# date created: 2-12-2020
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
awas_df = pd.read_pickle("./awas_data_df.pkl")
toga_df = pd.read_pickle("./toga_data_df.pkl")

################# -------------------- TOGA  -------------------- #################
# get mean in UT and BL for 1) flights in total and 2) individual flights 
toga_means = pd.DataFrame()

# all rf 
toga_means['UT - All RF'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)].mean()
toga_means['BL - All RF'] = toga_df.loc[(toga_df['GGALT'] < 2000)].mean()
# rf03
toga_means['UT - RF03'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF03')].mean()
toga_means['BL - RF03'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF03')].mean()
# rf04 
toga_means['UT - RF04'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF04')].mean()
toga_means['BL - RF04'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF04')].mean()
# rf05
toga_means['UT - RF05'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF05')].mean()
toga_means['BL - RF05'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF05')].mean()
# rf06
toga_means['UT - RF06'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF06')].mean()
toga_means['BL - RF06'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF06')].mean()
# rf07 
toga_means['UT - RF07'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF07')].mean()
toga_means['BL - RF07'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF07')].mean()
# rf08
toga_means['UT - RF08'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF08')].mean()
toga_means['BL - RF08'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF08')].mean()
# rf09
toga_means['UT - RF09'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF09')].mean()
toga_means['BL - RF09'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF09')].mean()
# rf10
toga_means['UT - RF10'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF10')].mean()
toga_means['BL - RF10'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF10')].mean()
# rf11
toga_means['UT - RF11'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF11')].mean()
toga_means['BL - RF11'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF11')].mean()
# rf12
toga_means['UT - RF12'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF12')].mean()
toga_means['BL - RF12'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF12')].mean()
# rf13
toga_means['UT - RF13'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF13')].mean()
toga_means['BL - RF13'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF13')].mean()
# rf14
toga_means['UT - RF14'] = toga_df.loc[(toga_df['GGALT'] > 12000) & (toga_df['GGALT'] < 14000)
                                                          & (toga_df['Flight'] == 'RF14')].mean()
toga_means['BL - RF14'] = toga_df.loc[(toga_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF14')].mean()

toga_means = toga_means.drop('GGALT').drop('GGLAT').drop('GGLON')
#toga_means.index.name = "Trace_Gas"
toga_means = toga_means.reset_index()
toga_means = toga_means.rename(columns={'index': 'Trace_Gas'})
toga_means.to_pickle("./toga_means.pkl")

# In[5]:


# ratios for 1) flights in total and 2) individual flights 
toga_ratios = pd.DataFrame()

toga_ratios['Trace_Gas'] = toga_means['Trace_Gas']
toga_ratios['All RF'] = toga_means['UT - All RF']/toga_means['BL - All RF']
toga_ratios['RF03'] = toga_means['UT - RF03']/toga_means['BL - RF03']
toga_ratios['RF04'] = toga_means['UT - RF04']/toga_means['BL - RF04']
toga_ratios['RF05'] = toga_means['UT - RF05']/toga_means['BL - RF05']
toga_ratios['RF06'] = toga_means['UT - RF06']/toga_means['BL - RF06']
toga_ratios['RF07'] = toga_means['UT - RF07']/toga_means['BL - RF07']
toga_ratios['RF08'] = toga_means['UT - RF08']/toga_means['BL - RF08']
toga_ratios['RF09'] = toga_means['UT - RF09']/toga_means['BL - RF09']
toga_ratios['RF10'] = toga_means['UT - RF10']/toga_means['BL - RF10']
toga_ratios['RF11'] = toga_means['UT - RF11']/toga_means['BL - RF11']
toga_ratios['RF12'] = toga_means['UT - RF12']/toga_means['BL - RF12']
toga_ratios['RF13'] = toga_means['UT - RF13']/toga_means['BL - RF13']
toga_ratios['RF14'] = toga_means['UT - RF14']/toga_means['BL - RF14']
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

################# -------------------- AWAS  -------------------- #################
# get mean in UT and BL for 1) flights in total and 2) individual flights 
awas_means = pd.DataFrame()

# all rf 
awas_means['UT - All RF'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)].mean()
awas_means['BL - All RF'] = awas_df.loc[(awas_df['GGALT'] < 2000)].mean()
# rf03
awas_means['UT - RF03'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF03')].mean()
awas_means['BL - RF03'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (toga_df['Flight'] == 'RF03')].mean()
# rf04 
awas_means['UT - RF04'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF04')].mean()
awas_means['BL - RF04'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF04')].mean()
# rf05
awas_means['UT - RF05'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF05')].mean()
awas_means['BL - RF05'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF05')].mean()
# rf06
awas_means['UT - RF06'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF06')].mean()
awas_means['BL - RF06'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF06')].mean()
# rf07 
awas_means['UT - RF07'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF07')].mean()
awas_means['BL - RF07'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF07')].mean()
# rf08
awas_means['UT - RF08'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF08')].mean()
awas_means['BL - RF08'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF08')].mean()
# rf09
awas_means['UT - RF09'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF09')].mean()
awas_means['BL - RF09'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF09')].mean()
# rf10
awas_means['UT - RF10'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF10')].mean()
awas_means['BL - RF10'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF10')].mean()
# rf11
awas_means['UT - RF11'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF11')].mean()
awas_means['BL - RF11'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF11')].mean()
# rf12
awas_means['UT - RF12'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF12')].mean()
awas_means['BL - RF12'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF12')].mean()
# rf13
awas_means['UT - RF13'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF13')].mean()
awas_means['BL - RF13'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF13')].mean()
# rf14
awas_means['UT - RF14'] = awas_df.loc[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)
                                                          & (awas_df['Flight'] == 'RF14')].mean()
awas_means['BL - RF14'] = awas_df.loc[(awas_df['GGALT'] < 2000) & (awas_df['Flight'] == 'RF14')].mean()

#toga_means = toga_means.transpose()
awas_means.index.name = "Trace_Gas"
awas_means = awas_means.drop('GGALT').drop('GGLAT').drop('GGLON')
awas_means.to_pickle("./awas_means.pkl")

# ratios for 1) flights in total and 2) individual flights 
awas_ratios = pd.DataFrame()

awas_ratios['All RF'] = awas_means['UT - All RF']/awas_means['BL - All RF']
awas_ratios['RF03'] = awas_means['UT - RF03']/awas_means['BL - RF03']
awas_ratios['RF04'] = awas_means['UT - RF04']/awas_means['BL - RF04']
awas_ratios['RF05'] = awas_means['UT - RF05']/awas_means['BL - RF05']
awas_ratios['RF06'] = awas_means['UT - RF06']/awas_means['BL - RF06']
awas_ratios['RF07'] = awas_means['UT - RF07']/awas_means['BL - RF07']
awas_ratios['RF08'] = awas_means['UT - RF08']/awas_means['BL - RF08']
awas_ratios['RF09'] = awas_means['UT - RF09']/awas_means['BL - RF09']
awas_ratios['RF10'] = awas_means['UT - RF10']/awas_means['BL - RF10']
awas_ratios['RF11'] = awas_means['UT - RF11']/awas_means['BL - RF11']
awas_ratios['RF12'] = awas_means['UT - RF12']/awas_means['BL - RF12']
awas_ratios['RF13'] = awas_means['UT - RF13']/awas_means['BL - RF13']
awas_ratios['RF14'] = awas_means['UT - RF14']/awas_means['BL - RF14']

awas_ratios = awas_ratios.reset_index()

# trop trace gas names column so doesnt get duplicated 
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
master_list.to_pickle("./contrast_ratios.pkl")

# look at output 
master_list


# test plot 
fig, ax = plt.subplots(figsize=(7, 5))
ax.set(xscale="log")
sns.scatterplot(data=master_list, x='BL_tau', y='All RF', hue='Instrument', ax = ax)
ax.set_xlim([10**-1, 10**5])
ax.set_title('Campaign Average')
ax.grid(which = 'major')
plt.show()


