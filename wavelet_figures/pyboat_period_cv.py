# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 13:43:50 2021

@author: william
@email: williams8645@gmail.com
"""

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

# CV vs period of each cell

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
        
        # select those traces that have period powers greater than 10
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        ridge_table = ridge_table.loc[ridge_table['traceId'].isin(select_trace)]
        
        # group by traceId
        rd_grp = ridge_table.groupby(['traceId'])
        
        # calculate mean periods and coefficient fo variance of the periods
        mean_period = rd_grp['periods'].mean()
        cov = rd_grp['periods'].std()/rd_grp['periods'].mean()
        
        # plot scatter plots with linear regression
        x = mean_period.values
        y = cov.values
        res = stats.linregress(x,y)
    
        ax = axs[int(i/6),j-1]
        scatter(ax)

        
        #plt.savefig('graph/%s_amp_vs_per.png' %file_name)

plt.setp(axs[-1, :], xlabel='Period (hour)')
plt.setp(axs[:, 0], ylabel='CV')
for i in range(6):
    cur_ax = axs[0,i]
    cur_ax.set_title('%s' % label_list[i],fontsize = 20)




# std vs period of each cell
for i in condition_dict:
    file_name = condition_dict[i]
    
    powers_series = pd.read_csv('wider_table/powerseries/%s_circadian_powerseries.csv'% file_name)
    ridge_table = pd.read_csv('wider_table/ridge_result/%s_circadian.csv' % file_name)
    
    # select those traces that have period powers greater than 10
    select_trace = powers_series.loc[powers_series['0']>10]['index']
    ridge_table = ridge_table.loc[ridge_table['traceId'].isin(select_trace)]
    
    # group by traceId
    rd_grp = ridge_table.groupby(['traceId'])
    
    # calculate mean periods and coefficient fo variance of the periods
    mean_period = rd_grp['periods'].mean()
    std = rd_grp['periods'].std()
    
    # plot scatter plots with linear regression
    x = mean_period.values
    y = std.values
    res = stats.linregress(x,y)
    
    fig, ax = plt.subplots()
    ax.scatter(x,y, s=20)
    ax.plot(x,res.intercept + res.slope*x, color='k')
    ax.text(min(x),max(y)-max(y)/10,'R-square = %.4f\nn = %d'% (res.rvalue**2, len(x)), fontsize=10)
    ax.set_xlabel('Period (hour)', fontsize = 20)
    ax.set_ylabel('Standard deviation (hour)', fontsize = 20)
    ax.set_title('%s std vs period' % file_name)
    plt.savefig('graph/%s_std_vs_period.png' %file_name)



# CV vs mean period of each condition
title_list = ['High density','Medium density',"Low density"]
color_list = ['tomato','orange','lime','cyan','b','orchid']
label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']

for i in [0,6,12]:
    x = []
    y = []
    fig, ax = plt.subplots()  
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]
    
        powers_series = pd.read_csv('wider_table/powerseries/%s_circadian_powerseries.csv'% file_name)
        ridge_table = pd.read_csv('wider_table/ridge_result/%s_circadian.csv' % file_name)
        
        # select those traces that have period powers greater than 10
        select_trace = powers_series.loc[powers_series['0']>10]['index']
        ridge_table = ridge_table.loc[ridge_table['traceId'].isin(select_trace)]
        
        # group by traceId
        rd_grp = ridge_table.groupby(['traceId'])
        
        # calculate mean periods and coefficient fo variance of the periods
        mean_period = rd_grp['periods'].mean()
        per = mean_period.mean()
        cov = mean_period.std()/mean_period.mean()
        
        # plot scatter plots with linear regression
        x.append(per)
        y.append(cov)
        ax.scatter(x[j-1],y[j-1],color=color_list[j-1],label=label_list[j-1])
    
    res = stats.linregress(x,y)
    ax.plot(x,[res.intercept + res.slope*a for a in x], color='k')
    ax.text(min(x),max(y),'R-square = %.4f'% res.rvalue**2, fontsize=10)
    ax.legend()
    ax.set_xlabel('Mean period (hour)', fontsize = 20)
    ax.set_ylabel('C.V.', fontsize = 20)
    ax.set_title('%s C.V. vs mean period' % title_list[int(i/6)])
    plt.savefig('graph/%s_cv_vs_mean_period.png' % title_list[int(i/6)])









