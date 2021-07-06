# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 09:28:28 2021

@author: william
"""

import pandas as pd
import os
import itertools
import matplotlib.pyplot as plt

os.chdir('D:/Charite/labA/WP2')

condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

count_before=0
count_after=0
ratio_list = []
for i in condition_dict:
    df = pd.read_csv('table_filtered_by_size/%s.csv' % condition_dict[i])
    
    df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
    
    # remove the traces that have similarity bigger than 80%
    remove_list = []
    pos_list = list(set(df['position']))
    for l in pos_list:
        df_pos = df.loc[df['position'] == l]
        lin_list = list(set(df_pos['lineageId']))
        for m in lin_list:
            df_pos_lin = df_pos.loc[df_pos['lineageId']==m]
            df_pivot = df_pos_lin.pivot(index = 'frame',
                                        columns = 'traceId',
                                        values = 'Mean.Intensity.c2')
            
            # because NaN will derive NaN, interpolate them to avoid cutting long traces short
            df_pivot.interpolate(method = 'linear', limit_direction = 'both', inplace = True)
            
            # pairwise comparison
            for j,k in itertools.combinations(df_pivot,2):
                if (k in remove_list):
                    continue
                sub = df_pivot[j]-df_pivot[k]
                count = sub.value_counts()
                if 0 in count.index:
                    ratio = count.loc[0]/(count.loc[0]+count.loc[~count.index.isin([0])].sum())
                    ratio_list.append(ratio)
                    if ratio > 0.8:
                        remove_list.append(k)
                        continue
    
    df_circadian = df.pivot(index = 'frame', columns = 'traceId', values = 'Mean.Intensity.c2')
    
    df_cell_cycle = df.pivot(index = 'frame', columns = 'traceId', values = 'Mean.Intensity.c3')
    
    count_before+=len(df_circadian.columns)
    
    # remove them
    df_circadian.drop(columns = remove_list,inplace = True)
    df_cell_cycle.drop(columns = remove_list,inplace = True)
    
    count_after+=len(df_circadian.columns)
    
    df_circadian.to_csv('./wider_table/%s_circadian.csv' % condition_dict[i])
    
    df_cell_cycle.to_csv('./wider_table/%s_cell_cycle.csv' % condition_dict[i])


# plot the ratio distribution
plt.hist(ratio_list)
plt.title('Similarity distribution')
plt.xlabel('Similarity')
plt.ylabel('Count')


# plot an example that was removed
df = pd.read_csv('table_filtered_by_size/%s.csv' % condition_dict[15])
    
df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)

df_circadian = df.pivot(index = 'frame', columns = 'traceId', values = 'Mean.Intensity.c2')

sub = df_circadian['301_14']-df_circadian['301_15']
count = sub.value_counts()
ratio = count.loc[0]/(count.loc[0]+count.loc[~count.index.isin([0])].sum())

plt.plot(df_circadian['301_14'].index*0.5,df_circadian['301_14'])
plt.xlabel('Time (hour)')
plt.ylabel('Circadian intensity (a.u.)')
plt.title('301_14')

plt.plot(df_circadian['301_15'].index*0.5,df_circadian['301_15'])
plt.xlabel('Time (hour)')
plt.ylabel('Circadian intensity (a.u.)')
plt.title('301_15')



