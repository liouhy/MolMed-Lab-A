# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 12:03:07 2021

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

# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})
label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
# high density
dts_df = pd.DataFrame()
for i in np.arange(1,7):
    file_name = condition_dict[i]
    df = pd.read_csv('table_filtered_by_size/%s.csv'% file_name)
    
    df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
    
    df_trace_grp = df.groupby(['traceId'])
    
    # create a division times series normalized to percentages
    dts = df_trace_grp['division'].sum().value_counts(normalize = True).sort_index()*100
    
    dts_df[i] = dts

dts_transpose = dts_df.T

dts_transpose.index = label_list
dts_transpose.columns.name = 'Division'
dts_transpose.columns = dts_transpose.columns.astype(int)

ax = dts_transpose.plot(kind = 'bar',stacked = True,rot=0)
ax.set_ylabel('Percentage (%)', fontsize = '20')
ax.tick_params(labelsize='12')
ax.set_title('High density', fontsize='25')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)





# medium density
dts_df = pd.DataFrame()
for i in np.arange(7,13):
    file_name = condition_dict[i]
    df = pd.read_csv('table_filtered_by_size/%s.csv'% file_name)
    
    df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
    
    df_trace_grp = df.groupby(['traceId'])
    
    # create a division times series normalized to percentages
    dts = df_trace_grp['division'].sum().value_counts(normalize = True).sort_index()*100
    
    dts_df[i] = dts

dts_transpose = dts_df.T

dts_transpose.index = label_list
dts_transpose.columns.name = 'Division'
dts_transpose.columns = dts_transpose.columns.astype(int)

ax = dts_transpose.plot(kind = 'bar',stacked = True,rot=0)
ax.set_ylabel('Percentage (%)', fontsize = '20')
ax.tick_params(labelsize='12')
ax.set_title('Medium density', fontsize='25')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)





# low density
dts_df = pd.DataFrame()
for i in np.arange(13,19):
    file_name = condition_dict[i]
    df = pd.read_csv('table_filtered_by_size/%s.csv'% file_name)
    
    df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
    
    df_trace_grp = df.groupby(['traceId'])
    
    # create a division times series normalized to percentages
    dts = df_trace_grp['division'].sum().value_counts(normalize = True).sort_index()*100
    
    dts_df[i] = dts

dts_transpose = dts_df.T

dts_transpose.index = label_list
dts_transpose.columns.name = 'Division'
dts_transpose.columns = dts_transpose.columns.astype(int)

ax = dts_transpose.plot(kind = 'bar',stacked = True,rot=0)
ax.set_ylabel('Percentage (%)', fontsize = '20')
ax.tick_params(labelsize='12')
ax.set_title('Low density', fontsize='25')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


