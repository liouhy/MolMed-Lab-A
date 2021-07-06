# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 15:25:59 2021
generate 2d histogram of cell cycle phases against circadian phases

@author: William
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random


os.chdir('D:/Charite/labA/WP2/wider_table')

condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

title_list = ['Untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                      '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
for i in [0,6,12]:
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]
        
        rd_cell_cycle = pd.read_csv('ridge_result/%s_cell_cycle.csv' % file_name)
        rd_cell_cycle.dropna(inplace = True)
        
        rd_circadian = pd.read_csv('ridge_result/%s_circadian.csv' % file_name)
        rd_circadian.dropna(inplace = True)
        
        # use powers_series to select finally filtered data
        powers_series = pd.read_csv('powerseries/%s_circadian_powerseries.csv'%file_name)
        
        select_index = powers_series.loc[powers_series['0']>10]['index']
        rd_cell_cycle = rd_cell_cycle.loc[rd_cell_cycle['traceId'].isin(select_index)]
        rd_circadian = rd_circadian.loc[rd_circadian['traceId'].isin(select_index)]
        
        x = rd_circadian['phase']/(2*np.pi)
        y = rd_cell_cycle['phase']/(2*np.pi)
        n = len(set(rd_circadian['traceId']))
        
        plt.hist2d(x,y,bins=np.arange(0,1.01,0.05),cmap=plt.cm.jet,density=True)
        plt.colorbar()
        plt.title('Low density'+ '(n = %d)'%n, fontsize='25')
        #plt.title(title_list[j-1]+' (n = %d)'%n, fontsize='25')
        plt.xlabel('Circadian phase ('+r'$\theta / 2\pi$'+')', fontsize='20')
        plt.ylabel('Cell cycle phase ('+r'$\theta / 2\pi$'+')', fontsize='20')
        plt.tick_params(labelsize='16')
        #plt.savefig('../graph/%s_ccp_vs_cp.png'%file_name)
        plt.show()
        plt.clf()


# randomly choose several traces
for i in [12]:
    for j in [1]:
        file_name = condition_dict[i+j]
        
        rd_cell_cycle = pd.read_csv('ridge_result/%s_cell_cycle.csv' % file_name)
        rd_cell_cycle.dropna(inplace = True)
        
        rd_circadian = pd.read_csv('ridge_result/%s_circadian.csv' % file_name)
        rd_circadian.dropna(inplace = True)
        
        # use powers_series to select finally filtered data
        powers_series = pd.read_csv('powerseries/%s_circadian_powerseries.csv'%file_name)
        
        select_index = powers_series.loc[powers_series['0']>10]['index']
        rd_cell_cycle = rd_cell_cycle.loc[rd_cell_cycle['traceId'].isin(select_index)]
        rd_circadian = rd_circadian.loc[rd_circadian['traceId'].isin(select_index)]
        
        # randomly select 50 traces
        random.seed(202)
        random_50 = random.sample(set(rd_cell_cycle['traceId']),114)
        
        rd_cell_cycle = rd_cell_cycle.loc[rd_cell_cycle['traceId'].isin(random_50)]
        rd_circadian = rd_circadian.loc[rd_circadian['traceId'].isin(random_50)]

        
        x = rd_circadian['phase']/(2*np.pi)
        y = rd_cell_cycle['phase']/(2*np.pi)
        n = len(set(rd_circadian['traceId']))
        
        plt.hist2d(x,y,bins=np.arange(0,1.01,0.05),cmap=plt.cm.jet,density=True)
        plt.colorbar()
        plt.title('Low density'+ ' (n = %d)'%n, fontsize='25')
        #plt.title(title_list[j-1]+' (n = %d)'%n, fontsize='25')
        plt.xlabel('Circadian phase ('+r'$\theta / 2\pi$'+')', fontsize='20')
        plt.ylabel('Cell cycle phase ('+r'$\theta / 2\pi$'+')', fontsize='20')
        plt.tick_params(labelsize='16')
        #plt.savefig('../graph/%s_ccp_vs_cp.png'%file_name)
        plt.show()
        plt.clf()




