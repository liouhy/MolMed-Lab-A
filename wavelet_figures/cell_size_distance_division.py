# -*- coding: utf-8 -*-
"""
Created on Mon May 31 14:33:46 2021

@author: user
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dirname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirname)
os.chdir('../')

condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

file_name = condition_dict[13]
df = pd.read_csv('./condition_table/%s.csv'%file_name)

df_group = df.groupby(['lineageId','position'])
df_groupcount = df_group.count()
df_groupcount.sort_values(by='frame',ascending=False,inplace=True)

lin, pos = df_groupcount.index[0]

filt = (df['position'] == pos) & (df['lineageId'] == lin)
df_lin = df.loc[filt]
print('traces:',set(df_lin['lineage']))
trace = int(input('select a trace:'))
df_trace = df_lin.loc[df_lin['lineage'] == trace]

x = df_trace['frame']
y = df_trace['Size_in_pixels_0']
y_c3 = df_trace['Mean.Intensity.c3']
fig, ax1 = plt.subplots()
ax1.plot(x,y,'k')
ax1.set_ylabel('size in pixels',color = 'k')
ax2 = ax1.twinx()
ax2.plot(x,y_c3,'b')
ax2.set_ylabel('Geminin',color = 'b')
ax2.tick_params('y',colors = 'b')

df_trace_distance = df_trace.set_index('frame').diff()[['xcenter','ycenter']]
df_trace_distance['distance'] = np.sqrt(df_trace_distance['xcenter']**2+df_trace_distance['ycenter']**2)
fig2, ax1 = plt.subplots()
ax1.plot(df_trace['frame'],df_trace_distance['distance'],'k')
ax1.set_ylabel('distance from previous time point',color = 'k')
ax2 = ax1.twinx()
ax2.plot(df_trace['frame'],df_trace['Size_in_pixels_0'],'b')
ax2.set_ylabel('size in pixels',color = 'b')

fig3, ax1 = plt.subplots()
ax1.plot(df_trace['frame'],df_trace_distance['distance'],'k')
ax1.set_ylabel('distance from previous time point',color = 'k')
ax2 = ax1.twinx()
ax2.plot(x,y_c3,'b')
ax2.set_ylabel('Geminin',color = 'b')
ax2.tick_params('y',colors = 'b')





