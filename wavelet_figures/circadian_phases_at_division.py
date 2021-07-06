# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 20:59:04 2021

@author: william
@gmail: williams8645@gmail.com
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle

os.chdir('D:/Charite/labA/WP2')

condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}



# get circadian phases at division (no interpolation)
phases_dict = {}
for k in condition_dict:
    file_name = condition_dict[k]
    df = pd.read_csv('table_filtered_by_size/%s.csv'% file_name)
    
    # to get the division time and traceId
    df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
    df_division = df.loc[df['division']==1,['frame','traceId']]
    
    
    rd = pd.read_csv('wider_table/ridge_result/%s_circadian.csv' % file_name)
    rd.set_index('frame',inplace = True)
    rd.dropna(inplace = True)
    
    # use powers_series to select finally filtered data
    powers_series = pd.read_csv('wider_table/powerseries/%s_circadian_powerseries.csv'%file_name)
    
    select_index = powers_series.loc[powers_series['0']>10]['index']
    rd_high_power = rd.loc[rd['traceId'].isin(select_index)]
    
    
    phases = []
    for i,j in zip(df_division['frame'],df_division['traceId']):
        row = rd_high_power.loc[(rd_high_power.index==i)&(rd_high_power['traceId']==j)]
        if len(row) !=0:
            phases.append(row.iloc[0,2])
    
    phases = [x/(2*np.pi) for x in phases]
    phases_dict[k] = phases


a_file = open("wider_table/phases_dict_no_interpolation.pkl", "wb")
pickle.dump(phases_dict, a_file)
a_file.close()





# plot polar barplots (no need to run above script!)
a_file = open("wider_table/phases_dict_no_interpolation.pkl", "rb")
phases_dict = pickle.load(a_file)
a_file.close()



for i in condition_dict:
    theta = np.linspace(0.0,2*np.pi,20,endpoint=False)
    n,bins,patches=plt.hist(phases_dict[i],bins=np.arange(0,1.01,0.05))
    width = 2*np.pi/20
    ax = plt.subplot(projection='polar')
    ax.bar(theta, n, width = width, bottom=0.0, edgecolor='w')
    ax.set_title('%s division at circadian phase' % condition_dict[i])
    plt.savefig('graph/%s_circadian_phase_at_division_polar.png'%condition_dict[i])
    plt.clf()



# plot histograms
for i in condition_dict:
    fig, ax = plt.subplots()
    n,bins,patches=ax.hist(phases_dict[i],edgecolor='w',bins=np.arange(0,1.01,0.05))
    ax.set_title('%s division at circadian phase' % condition_dict[i])
    ax.set_xlabel('Circadian phase ('+r'$\theta / 2\pi$'+')')
    ax.set_ylabel('Count')
    plt.savefig('graph/%s_circadian_phase_at_division.png'%condition_dict[i])
    
