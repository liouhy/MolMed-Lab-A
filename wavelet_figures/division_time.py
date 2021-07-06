# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 18:18:39 2021

@author: user
"""

import os
import pandas as pd
import numpy as np
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

# create division time table, division time is difined by the time needed for the next division
for i in condition_dict:
    file_name = condition_dict[i]
    df = pd.read_csv('table_filtered_by_size/%s.csv'% file_name)
    
    # only select rows when division
    df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
    df_division = df.loc[df['division']==1,['frame','traceId']]
    
    # calculate division time
    traceId_grp = df_division.groupby(['traceId'])
    division_time = traceId_grp['frame'].diff(-1).abs()/2
    df_division['division_time'] = division_time
    
    # remove rows with nan
    df_division.dropna(inplace=True)
    
    df_division.to_csv('division_time_table/%s.csv' % file_name, index=False)
    


# plot superimposed division time density
# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})

for i in [0,6,12]:
    x = np.arange(0,80,0.5)
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['red','orange','lime','cyan','b','orchid']
    label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
    fig, ax = plt.subplots(figsize=(6,3))
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]
        
        df_division = pd.read_csv('division_time_table/%s.csv' % file_name)
        
        kde = stats.gaussian_kde(df_division['division_time'])
        ax.plot(x,kde(x),color=color_list[j-1],label=label_list[j-1])
        
    #plt.xlim(10,110)
    ax.legend()
    ax.set_xlabel('Division time (hour)',fontsize='20')
    ax.set_ylabel('Density',fontsize='20')
    ax.tick_params(labelsize='16')
    ax.set_title(title_list[int(i/6)], fontsize='25')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig('graph/%s_division_time_density.png'%title_list[int(i/6)])    





    
# plot division time at circadian phase (scatter plot)

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
        rd_circadian = pd.read_csv('wider_table/ridge_result/%s_circadian.csv'%file_name)
    
        # use powers_series to select finally filtered data
        powers_series = pd.read_csv('wider_table/powerseries/%s_circadian_powerseries.csv'%file_name)
        
        select_index = powers_series.loc[powers_series['0']>10]['index']
        
        rd_circadian = rd_circadian.loc[rd_circadian['traceId'].isin(select_index)]
        
        # find circadian phase
        df_division = pd.read_csv('division_time_table/%s.csv' % file_name)
        df_division.set_index(['frame','traceId'], inplace=True)
        
        rd_circadian.set_index(['frame','traceId'], inplace=True)
        rd_circadian = rd_circadian['phase']
        
        dt_phase = pd.concat([df_division,rd_circadian],axis=1,join='inner')
        
        # scatter plot
        x=dt_phase['phase']/(2*np.pi)
        y=dt_phase['division_time']
        res = stats.linregress(x,y)
        
        ax = axs[int(i/6),j-1]
        scatter(ax)
    


plt.setp(axs[-1, :], xlabel='Circadian phase ('+r'$\theta / 2\pi$'+')')
plt.setp(axs[:, 0], ylabel='Division time (hour)')
for i in range(6):
    cur_ax = axs[0,i]
    cur_ax.set_title('%s' % label_list[i],fontsize = 20)









