# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 10:57:53 2021
re-do pyboat analysis without amplitude normalization to get amplitudes
@author: william
@email: williams8645@gmail.com
"""

import numpy as np
from pyboat import WAnalyzer
import os 
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from scipy import stats
from pyboat import ensemble_measures as em

os.chdir('D:/Charite/labA/WP2')


condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

# create tables with ridge results without amplitude normalization
for j in condition_dict:
    file_name = condition_dict[j]+'_circadian'
         
    df = pd.read_csv('wider_table/%s.csv'% file_name)
    df.set_index('frame', inplace = True)
    
    df_preprocess = pd.DataFrame(columns = df.columns, index = df.index)
    
    # detrend and amplitude normalize the signals
    dt = 0.5
    p = np.linspace(12,36,400)
    T_c = 36
                
    wAn = WAnalyzer(p, dt)
        
    for i in df:
        signal = df[i].dropna()   
        detr_signal = wAn.sinc_detrend(signal, T_c=T_c)
        
        df_preprocess[i] = detr_signal
    
    
    # get the the individual ridge readouts
    ridge_table = pd.DataFrame()
    
    # get the powers
    for i in df_preprocess:
        detr_signal = df_preprocess[i].dropna()
        wAn.compute_spectrum(detr_signal, do_plot = False) #False to not show each spectrum plot
        rd = wAn.get_maxRidge(power_thresh = 0, smoothing_wsize = 5)
        
        rd.set_index(detr_signal.index,inplace=True)
        
        rd['traceId'] = i
        ridge_table = ridge_table.append(rd)
    
    ridge_table = ridge_table.reset_index()
    ridge_table.to_csv('wider_table/ridge_result/%s_amp.csv' % file_name, index=False)




# get ensemble dynamics  
for i in condition_dict:
    ridge_results = {}
    t = 10
    file_name = condition_dict[i]+'_circadian'
    powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
    powers_series.set_index('index',inplace=True)
    
    ridge_table = pd.read_csv('wider_table/ridge_result/%s_amp.csv'%file_name)
    ridge_table.set_index('frame',inplace=True)
    traceId_list = list(set(ridge_table['traceId']))
    
    #create ridge_results dict
    for k in traceId_list:
        table = ridge_table.loc[ridge_table['traceId']==k]
        ridge_results[k] = table.drop(columns='traceId')
    
    select_index = powers_series.loc[powers_series['0']>10].index
    high_power_ridge_results = [ridge_results[i] for i in select_index]
    
    amplitudes = pd.concat([r['amplitude'] for r in high_power_ridge_results], axis = 1)
    amplitudes_mq1q3 = pd.DataFrame()
    amplitudes_mq1q3['median'] = amplitudes.median(axis = 1, skipna = True)
    amplitudes_mq1q3['Q1'] = amplitudes.quantile(q = 0.25, axis = 1)
    amplitudes_mq1q3['Q3'] = amplitudes.quantile(q = 0.75, axis = 1)
    
    amplitudes_mq1q3.to_csv('wider_table/ED/%s_ED_amp_no_norm_high_power.csv'%file_name)




# get ensemble dynamics (not selected by powers)
for i in condition_dict:
    ridge_results = {}
    t = 10
    file_name = condition_dict[i]+'_circadian'
    powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
    powers_series.set_index('index',inplace=True)
    
    ridge_table = pd.read_csv('wider_table/ridge_result/%s_amp.csv'%file_name)
    ridge_table.set_index('frame',inplace=True)
    traceId_list = list(set(ridge_table['traceId']))
    
    #create ridge_results dict
    for k in traceId_list:
        table = ridge_table.loc[ridge_table['traceId']==k]
        ridge_results[k] = table.drop(columns='traceId')
    
    select_index = powers_series.loc[powers_series['0']>1].index
    high_power_ridge_results = [ridge_results[i] for i in select_index]
    
    amplitudes = pd.concat([r['amplitude'] for r in high_power_ridge_results], axis = 1)
    amplitudes_mq1q3 = pd.DataFrame()
    amplitudes_mq1q3['median'] = amplitudes.median(axis = 1, skipna = True)
    amplitudes_mq1q3['Q1'] = amplitudes.quantile(q = 0.25, axis = 1)
    amplitudes_mq1q3['Q3'] = amplitudes.quantile(q = 0.75, axis = 1)
    
    amplitudes_mq1q3.to_csv('wider_table/ED/%s_ED_amp_no_norm.csv'%file_name)        
        


# plot ensemble dynamic results (amplitudes, high power)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        amplitudes = pd.read_csv('wider_table/ED/%s_ED_amp_no_norm_high_power.csv'%file_name)
        ax.plot(amplitudes['frame']/2,amplitudes['median'],color=color_list[j-1],label=label_list[j-1])
        

    ax.legend()
    ax.set_xlabel('Time (hour)')

    ax.set_ylabel('Amplitudes (a.u.)')

    ax.set_title(title_list[int(i/6)]+' '+'power > 10')

    plt.savefig('graph/%s_circadian_amp_no_norm_high_power.png'%title_list[int(i/6)])



# plot ensemble dynamic results (amplitudes, no power selection)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        amplitudes = pd.read_csv('wider_table/ED/%s_ED_amp_no_norm.csv'%file_name)
        ax.plot(amplitudes['frame']/2,amplitudes['median'],color=color_list[j-1],label=label_list[j-1])
        

    ax.legend()
    ax.set_xlabel('Time (hour)')

    ax.set_ylabel('Amplitudes (a.u.)')

    ax.set_title(title_list[int(i/6)])

    plt.savefig('graph/%s_circadian_amp_no_norm.png'%title_list[int(i/6)])


# plot boxplot of amplitudes with high powers
for i in [0,6,12]:
    fig, ax = plt.subplots()
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    amplitudes_list = []
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s_amp.csv'%file_name)
        
        traceId_grp = ridge_table.groupby(['traceId'])
        amplitudes_series = traceId_grp['amplitude'].median()
        
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        amplitudes_series = amplitudes_series.loc[amplitudes_series.index.isin(select_trace)]
        
        amplitudes_list.append(amplitudes_series)
    ax.boxplot(amplitudes_list)
    ax.set_ylabel('Amplitude (a.u.)')
    ax.set_xticklabels(label_list)
    ax.set_title(title_list[int(i/6)]+' '+'high power')
    plt.savefig('graph/%s_circadian_amp_high_power_box.png'%title_list[int(i/6)])


# plot boxplot of amplitudes (no power selection)
for i in [0,6,12]:
    fig, ax = plt.subplots()
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    amplitudes_list = []
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s_amp.csv'%file_name)
        
        traceId_grp = ridge_table.groupby(['traceId'])
        amplitudes_series = traceId_grp['amplitude'].median()
        
        select_trace = powers_series.loc[powers_series['0']>1]['index']
        amplitudes_series = amplitudes_series.loc[amplitudes_series.index.isin(select_trace)]
        
        
        amplitudes_list.append(amplitudes_series)
    ax.boxplot(amplitudes_list)
    ax.set_ylabel('Amplitude (a.u.)')
    ax.set_xticklabels(label_list)
    ax.set_title(title_list[int(i/6)])
    plt.savefig('graph/%s_circadian_amp_box.png'%title_list[int(i/6)])


# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})
def set_axis(ax,xlabel,ylabel):
    ax.set_ylabel(ylabel, fontsize='20')
    ax.tick_params(labelsize='16')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


# overlay density of amplitudes (no power selection)
for i in [0,6,12]:
    x=np.arange(0,500,5)
    fig, ax = plt.subplots(figsize=(6,3))
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['red','orange','lime','cyan','b','orchid']
    label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
    amplitudes_list = []
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s_amp.csv'%file_name)
        
        traceId_grp = ridge_table.groupby(['traceId'])
        amplitudes_series = traceId_grp['amplitude'].median()
        
        select_trace = powers_series.loc[powers_series['0']>1]['index']
        amplitudes_series = amplitudes_series.loc[amplitudes_series.index.isin(select_trace)]
        
        kde = stats.gaussian_kde(amplitudes_series)
        ax.plot(x,kde(x),color=color_list[j-1],label=label_list[j-1])
    ax.legend()
    ax.set_xlabel('Amplitude (a.u.)',fontsize='20')
    ax.set_ylabel('Density', fontsize='20')
    ax.tick_params(labelsize='16')
    #ax.set_title(title_list[int(i/6)], fontsize='25')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig('graph/%s_circadian_amp_box.png'%title_list[int(i/6)])


# scatter plot, median amplitude against period

# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})
label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
def scatter(ax):
    ax.scatter(x,y,s=10)
    ax.plot(x,res.intercept + res.slope*x, color='k')
    ax.text(min(x),max(y)-max(y)/5,'R-square = %.4f\nn = %d'% (res.rvalue**2, len(x)), fontsize=10)
    #ax.set_title('%s' % label_list[j-1],fontsize = 25)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

fig, axs = plt.subplots(3,6,figsize=(18,8))

for i in [0,6,12]:
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]
        
        powers_series = pd.read_csv('wider_table/powerseries/%s_circadian_powerseries.csv'% file_name)
        ridge_table_amp = pd.read_csv('wider_table/ridge_result/%s_circadian_amp.csv' % file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s_circadian.csv' % file_name)
        
        # select those traces that have period powers greater than 10
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        ridge_table_amp = ridge_table_amp.loc[ridge_table_amp['traceId'].isin(select_trace)]
        ridge_table = ridge_table.loc[ridge_table['traceId'].isin(select_trace)]
        
        # group by traceId
        rd_amp_grp = ridge_table_amp.groupby(['traceId'])
        rd_grp = ridge_table.groupby(['traceId'])
        
        # calculate mean periods and median amplitudes
        median_amp = rd_amp_grp['amplitude'].median()
        mean_period = rd_grp['periods'].mean()
        merge = pd.concat([median_amp,mean_period], axis = 1)
        
        # calculate the linear regression
        x = merge['periods'].values
        y = merge['amplitude'].values
        res = stats.linregress(x,y)
        
        # plot scatter plots
        ax = axs[int(i/6),j-1]
        scatter(ax)

        
        #plt.savefig('graph/%s_amp_vs_per.png' %file_name)

plt.setp(axs[-1, :], xlabel='Period (hour)',)
plt.setp(axs[:, 0], ylabel='Amplitude (a.u.)')
for i in range(6):
    cur_ax = axs[0,i]
    cur_ax.set_title('%s' % label_list[i],fontsize = 20)









