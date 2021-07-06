# -*- coding: utf-8 -*-
"""
Created on Wed Jun 2 10:42:30 2021

@author: William
@email: williams8645@gmail.com
"""

import numpy as np
#import matplotlib.pyplot as plt
import os 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

os.chdir('D:/Charite/labA/WP2')


condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}




# plot overlayed period density with high power
for i in [0,6,12]:
    fig, ax = plt.subplots()
    x=np.arange(0,50,0.5)
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated',r'$0\muM$','1.25uM','2.5uM','5uM','10uM']
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s.csv'%file_name)
        
        traceId_grp = ridge_table.groupby(['traceId'])
        periods_series = traceId_grp['periods'].mean()
        
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        periods_series = periods_series.loc[periods_series.index.isin(select_trace)]
        
        kde = stats.gaussian_kde(periods_series)
        ax.plot(x,kde(x),color=color_list[j-1],label=label_list[j-1])
    ax.legend()
    ax.set_xlabel('Period (hour)')
    ax.set_ylabel('Density')
    ax.set_title(title_list[int(i/6)]+' '+'high power')
    plt.savefig('graph/%s_circadian_high_power.png'%title_list[int(i/6)])
    plt.clf()




# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})
def set_axis(ax,xlabel,ylabel):
    ax.set_ylabel(ylabel, fontsize='20')
    ax.tick_params(labelsize='16')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


# plot boxplot of periods with high powers
for i in [0,6,12]:
    fig, ax = plt.subplots(figsize=(6,3))
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
    periods_list = []
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s.csv'%file_name)
        
        traceId_grp = ridge_table.groupby(['traceId'])
        periods_series = traceId_grp['periods'].mean()
        
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        periods_series = periods_series.loc[periods_series.index.isin(select_trace)]
        
        periods_list.append(periods_series)
    plt.ylim(10,40)
    ax.boxplot(periods_list)
    ax.set_ylabel('Period (hour)',fontsize='20')
    ax.set_xticklabels(label_list)
    ax.tick_params(labelsize='15')
    ax.set_title(title_list[int(i/6)],fontsize='25')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig('graph/%s_circadian_high_power_box.png'%title_list[int(i/6)])
    



"""
# plot boxplot of periods (no power selection)
# list_dict index: 1:untreated, 2:0uM, 3:1.25uM, 4:2.5uM, 5:5uM, 6:10uM
list_dict = {}
for i in [1,2,3,4,5,6]:
    periods_list = []
    for j in [0,6,12]:
        file_name = condition_dict[i+j]+'_circadian'
        ridge_table = pd.read_csv('wider_table/ridge_result/%s.csv'%file_name)
        
        traceId_grp = ridge_table.groupby(['traceId'])
        periods_series = traceId_grp['periods'].median()
        
        periods_list.append(periods_series)
    
    list_dict[i] = periods_list
    
    
ticks = ['High density','Medium density',"Low density"]

plt.figure(figsize=(6,3))

plt.boxplot(list_dict[1], positions=np.arange(1,4)-0.25,widths=0.1)
plt.boxplot(list_dict[2], positions=np.arange(1,4)-0.15,widths=0.1)
plt.boxplot(list_dict[3], positions=np.arange(1,4)-0.05,widths=0.1)
plt.boxplot(list_dict[4], positions=np.arange(1,4)+0.05,widths=0.1)
plt.boxplot(list_dict[5], positions=np.arange(1,4)+0.15,widths=0.1)
plt.boxplot(list_dict[6], positions=np.arange(1,4)+0.25,widths=0.1)

plt.xticks(np.arange(1,4),ticks)
"""


