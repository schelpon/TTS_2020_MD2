#!/usr/bin/env python
# coding: utf-8
# prep for tts segment analysis 
# want to isolate each awas cannister in the UT and get TOGA measurements within time span
# date created: 2/28/2020
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

#### ------------------- TIME SPAN 
# 6 minutes total, 3 mins of either side of awas collection 
m = 6
speed = 235.4 #m/s
dist_km = (speed*(m*60))/1000
dist_km

#### ------------------- LOAD IN 
awas_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/awas_data_df.pkl")
toga_df = pd.read_pickle("/UTLS/schelpon/TTS_2020/get_ratios/toga_data_df.pkl")

#### ------------------- ISOLATE AWAS SEGMENTS IN THE UT 
awas_df_ut = awas_df[(awas_df['GGALT'] > 12000) & (awas_df['GGALT'] < 14000)]
awas_df_ut.reset_index()

#### ------------------- GET TOGA SEGMENTS THAT CORRESPOND TO AWAS TIMES 
# make a new dataframe for toga with AWAS time, plus average of all tracers in the segment
# want one UT value per segment 
toga_segments = pd.DataFrame()
for col in toga_df.columns: 
	toga_segments[col] = ''
toga_segments = toga_segments.drop(columns = 'Notes')

# grab everything TOGA +/- 3 minutes from that awas sample 
for idx in awas_df_ut.iterrows():
    t = idx[1].Time_UTC
    # ----- get time of awas sample, +/- 3 minutes
    m = 3
    s = 60*m
    ts = t - datetime.timedelta(0,s)
    te = t + datetime.timedelta(0,s) 
    # ----- get toga segment that corresponds to that time 
    toga_seg = toga_df[(toga_df.Time_UTC > ts) & (toga_df.Time_UTC < te)]
    toga_seg_sum = toga_seg.mean()
    # ----- if there are toga meas in that time, append 
    if (len(toga_seg) > 0):
        # ----- fill in what was lost from mean 
        time = pd.Series({'Time_UTC': t})
        flight = pd.Series({'Flight': toga_seg['Flight'].iloc[0]})
        inst = pd.Series({'Intrument': 'TOGA'})
        toga_seg_toappend = pd.DataFrame(pd.concat([time, flight, inst, toga_seg_sum]))
        toga_seg_toappend = toga_seg_toappend.transpose()
        # add to dataframe! 
        toga_segments = toga_segments.append(toga_seg_toappend, ignore_index=True)
    else:
        toga_seg_filled = toga_seg
        toga_seg_filled = toga_seg_filled.drop(columns = 'Notes')
        # fill ins, qualitative 
        time = pd.Series({'Time_UTC': t})
        flight = idx[1].Flight
        ggalt = idx[1].GGALT
        gglat = idx[1].GGLAT
        gglon = idx[1].GGLON
        inst = pd.Series({'Intrument': 'TOGA'})
        # tracers make nan 
        toga_seg_filled = toga_seg_filled.append(pd.Series(), ignore_index=True)
        toga_seg_filled['Time_UTC'] = t
        #toga_seg_filled['Flight'] = flight[0]
        toga_seg_filled['Flight'] = flight
        toga_seg_filled['Intrument'] = inst[0]
        toga_seg_filled['GGALT'] = ggalt
        toga_seg_filled['GGLAT'] = gglat
        toga_seg_filled['GGLON'] = gglon
        # add to dataframe
        toga_segments = toga_segments.append(toga_seg_filled, ignore_index=True)




#### ------------------- pickle and save 
awas_segments = awas_df_ut
awas_segments.to_pickle("./awas_segments.pkl")
toga_segments.to_pickle("./toga_segments.pkl")


