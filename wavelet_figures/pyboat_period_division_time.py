# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 14:43:51 2021

@author: user
"""

import os 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

os.chdir('D:/Charite/labA/WP2')


condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

# scatter plots, mean division time vs period

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
        ridge_table = pd.read_csv('wider_table/ridge_result/%s_circadian.csv' % file_name)
        division_table = pd.read_csv('division_time_table/%s.csv' % file_name)
        
        # select those traces that have period powers greater than 10
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        ridge_table = ridge_table.loc[ridge_table['traceId'].isin(select_trace)]
        
        # group by traceId
        rd_grp = ridge_table.groupby(['traceId'])
        
        # calculate mean periods and coefficient fo variance of the periods
        mean_period = rd_grp['periods'].mean()
        
        
        # calculate mean division time
        mean_dt = division_table.groupby(['traceId'])['division_time'].mean()
        
        # join two table, only take the intersected traces
        period_dt = pd.concat([mean_period,mean_dt], axis=1, join='inner')
        
            
        #plot mean division time vs
        x = period_dt['periods'].values
        y = period_dt['division_time'].values
        res = stats.linregress(x,y)
        
        ax = axs[int(i/6),j-1]
        scatter(ax)
    
    
plt.setp(axs[-1, :], xlabel='Period (hour)',)
plt.setp(axs[:, 0], ylabel='Mean division time (hour)')
for i in range(6):
    cur_ax = axs[0,i]
    cur_ax.set_title('%s' % label_list[i],fontsize = 20)














