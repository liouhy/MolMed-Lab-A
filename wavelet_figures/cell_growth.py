# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 21:10:03 2021

@author: user
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


os.chdir('D:/Charite/labA/WP2')
table_path = 'D:/Charite/labA/WP1/Large_scale_image_processing/Mydata/Output'

condition_combine_dict = {101:'high_density_untreated',81:'high_density_0uM',61:'high_density_1.25uM',
             41:'high_density_2.5uM',21:'high_density_5uM',1:'high_density_10uM',
             121:'medium_density_untreated',141:'medium_density_0uM',161:'medium_density_1.25uM',
             181:'medium_density_2.5uM',201:'medium_density_5uM',221:'medium_density_10uM',
             341:'low_density_untreated',321:'low_density_0uM',301:'low_density_1.25uM',
             281:'low_density_2.5uM',261:'low_density_5uM',241:'low_density_10uM'}





# get low_density_untreated cell numbers at frame 0 as normalizing value
count_0 = 0
for i in range(20):
    df = pd.read_csv('%s/xy%03d/xy%03d-t_tracking_table.csv' % (table_path, 341+i, 341+i))
    c = len(set(df.loc[df['frame']==0]['trackId']))
    count_0 += c




# count cell numbers for each condition over frames, and save into a dictionary
count_dict = {}
for j in condition_combine_dict:    
    count_list = [0 for x in range(232)]
    for i in range(20):
        df = pd.read_csv('%s/xy%03d/xy%03d-t_tracking_table.csv' % (table_path, j+i, j+i))
        
        count_list_pos = []
        for k in range(232):
            c = len(set(df.loc[df['frame']==k]['trackId']))
            count_list_pos.append(c)
            
        count_list = [(l+m) for l,m in zip(count_list,count_list_pos)]
    
    count_list = [x/count_0 for x in count_list]
    count_dict[j] = count_list

 
# plot results
pos_list = [ x for x in condition_combine_dict]
title_list = ['High density','Medium density',"Low density"]
color_list = ['tomato','orange','lime','cyan','b','orchid']
label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
for i in range(3):
    fig, ax = plt.subplots()
    for j in range(6):
        index = pos_list[i*6+j]
        ax.plot(np.arange(0,116,0.5),count_dict[index], label = label_list[j], color = color_list[j])
    
    ax.legend()
    ax.set_title(title_list[i],fontsize = 30)
    ax.set_xlabel('Time (hour)',fontsize = 20)
    ax.set_ylabel('Normalized cell counts',fontsize = 20)













 
    
    