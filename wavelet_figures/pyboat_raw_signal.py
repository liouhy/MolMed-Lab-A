# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 20:08:28 2021

@author: user
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from pyboat import WAnalyzer
import numpy as np

os.chdir('D:/Charite/labA/WP1/Large_scale_image_processing/Mydata/Output')
condition_combine_dict = {101:'high_density_untreated',81:'high_density_0uM',61:'high_density_1.25uM',
             41:'high_density_2.5uM',21:'high_density_5uM',1:'high_density_10uM',
             121:'medium_density_untreated',141:'medium_density_0uM',161:'medium_density_1.25uM',
             181:'medium_density_2.5uM',201:'medium_density_5uM',221:'medium_density_10uM',
             341:'low_density_untreated',321:'low_density_0uM',301:'low_density_1.25uM',
             281:'low_density_2.5uM',261:'low_density_5uM',241:'low_density_10uM',
             361:'very_low_density_untreated',381:'very_low_density_0uM',401:'very_low_density_1.25uM'}


# ensemble raw circadian signal for each condition by their median
sig_df = pd.DataFrame()
pos_start = [1,21,41,61,81,101,121,141,161,181,201,221,241,261,281,301,321,341,361,381,401]
for j in pos_start:
    
    sig_dict = {}
    for i in range(232):
        sig_dict[i]=[]
    
    for i in range(20):
        pos = i + j

        df_c2 = pd.read_csv('xy%03d/xy%03dchannel2intensities_table.csv' %(pos,pos))

        
        for k in range(232):
            cur_sig = list(df_c2.loc[df_c2['timestep']==k]['Mean Intensity'])
            sig_dict[k].extend(cur_sig)
        
        
        
        #df_c2_grp = df_c2.groupby(['timestep'])
        #circadian_sig = df_c2_grp['Mean Intensity'].median()
        #circadian_df = pd.concat([circadian_df,circadian_sig],axis=1)
    
    
    sig_median=[]
    for i in range(232):
        sig_median.append(np.median(sig_dict[i]))
    
    sig_df[j] = sig_median

sig_df.to_csv('D:/Charite/labA/WP2/raw_circadian_median.csv',index=False)




# make plots
sig_df = pd.read_csv('D:/Charite/labA/WP2/raw_circadian_median.csv')

# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})

# detrend before plotting
# high density
fig,ax = plt.subplots(figsize=(6,4))
for i in [5,4,3,2,1,0]:
    pos = pos_start[i]
    
    color_list = ['orchid','b','cyan','lime','orange','red']
    label_list = ['10'+r'$\mu$'+'M','5'+r'$\mu$','2.5'+r'$\mu$'+'M','1.25'+r'$\mu$'+'M',
                  'DMSO','untreated']
    
    dt = 0.5
    p = np.linspace(12,36,400)
    T_c = 36
    
    wAn = WAnalyzer(p, dt)
    signal = sig_df[pos]
    smooth_signal = wAn.sinc_smooth(signal, 5)
    detr_signal = wAn.sinc_detrend(smooth_signal, T_c=T_c)
    #norm_signal = wAn.normalize_amplitude(detr_signal, window_size = 36)

    x=np.arange(len(detr_signal))/2
    y=detr_signal
    ax.plot(x,y,color=color_list[i],label=label_list[i])

ax.legend()
ax.set_title('High density', fontsize='25')
ax.set_xlabel('Time (hour)', fontsize='20')
ax.set_ylabel('Mean intensity', fontsize='20')
ax.tick_params(labelsize='16')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


# medium density
fig,ax = plt.subplots(figsize=(6,4))
c=0
for i in np.arange(6,12):
    pos = pos_start[i]
    
    color_list = ['red','orange','lime','cyan','b','orchid']
    label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
    
    dt = 0.5
    p = np.linspace(12,36,400)
    T_c = 36
    
    wAn = WAnalyzer(p, dt)
    signal = sig_df[pos]
    smooth_signal = wAn.sinc_smooth(signal, 5)
    detr_signal = wAn.sinc_detrend(smooth_signal, T_c=T_c)
    #norm_signal = wAn.normalize_amplitude(detr_signal, window_size = 36)

    x=np.arange(len(detr_signal))/2
    y=detr_signal
    ax.plot(x,y,color=color_list[c],label=label_list[c])
    c+=1

ax.legend()
ax.set_title('Medium density', fontsize='25')
ax.set_xlabel('Time (hour)', fontsize='20')
ax.set_ylabel('Mean intensity', fontsize='20')
ax.tick_params(labelsize='16')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


# low density
fig,ax = plt.subplots(figsize=(6,4))
c=0
for i in [17,16,15,14,13,12]:
    pos = pos_start[i]
    
    color_list = ['red','orange','lime','cyan','b','orchid']
    label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
    
    dt = 0.5
    p = np.linspace(12,36,400)
    T_c = 36
    
    wAn = WAnalyzer(p, dt)
    signal = sig_df[pos]
    smooth_signal = wAn.sinc_smooth(signal, 5)
    detr_signal = wAn.sinc_detrend(smooth_signal, T_c=T_c)
    #norm_signal = wAn.normalize_amplitude(detr_signal, window_size = 36)

    x=np.arange(len(detr_signal))/2
    y=detr_signal
    ax.plot(x,y,color=color_list[c],label=label_list[c])
    c+=1

ax.legend()
ax.set_title('Low density', fontsize='25')
ax.set_xlabel('Time (hour)', fontsize='20')
ax.set_ylabel('Mean intensity', fontsize='20')
ax.tick_params(labelsize='16')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

