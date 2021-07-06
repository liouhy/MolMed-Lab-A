# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:09:14 2021

@author: user
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

os.chdir('D:\Charite\labA\WP2')

condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}


def filter_by_size():   
    #create a position list to iterate on
    pos_list = list(set(df['position']))
    
    #create an empty dataframe
    df_new = pd.DataFrame(columns = df.columns)
    
    #iterate on different positions
    for k in pos_list:
        df_pos = df.loc[df['position'] == k]
        trace_list = list(set(df_pos['lineage']))
            
        #create an empty dataframe
        df_pos_new = pd.DataFrame(columns = df.columns)
             
        #loop on the traces, create the tables and combine them with the initiated table
        for j in trace_list:
            trace = j
            df_trace = df_pos.loc[df_pos['lineage'] == trace]
            
            df_trace.set_index('frame', inplace = True)
            size_diff = df_trace.diff()['Size_in_pixels_0']
            
            for i in df_trace.index:
                d = size_diff.loc[i]
                if (d>500) or (d<-500):
                    if df_trace.loc[(i-10):(i+10),'division'].sum() == 0:
                        df_trace = df_trace.loc[0:i]
                        break
                    else:
                        continue
                else:
                    continue
            
            if len(df_trace) > 100:
                df_trace.reset_index(inplace = True)
                df_pos_new = df_pos_new.append(df_trace)
            else:
                continue
        df_new = df_new.append(df_pos_new)
    return df_new

for l in condition_dict:
    file_name = condition_dict[l]
    df = pd.read_csv('./condition_table_division/%s.csv'%file_name)
    df_new = filter_by_size()
    df_new.to_csv('./table_filtered_by_size/%s.csv'%condition_dict[l],index = False)
    
    
#export plots to visualize the result.
#In each condition, I selected 2 positons, in each of which I further selected 3 traces to plot
from matplotlib.backends.backend_pdf import PdfPages


#opend a mutlipage pdf
pp = PdfPages('./table_filtered_by_size/Geminin_circadian_division.pdf')
for i in condition_dict:
    file_name = condition_dict[i]
    df = pd.read_csv('./table_filtered_by_size/%s.csv'%file_name)
    pos_list = list(set(df['position']))
    
    for j in range(2):
        pos = pos_list[j]
        df_pos = df.loc[df['position'] == pos]
        trace_list = list(set(df_pos['lineage'])) 
        
        for k in range(3):
            trace = trace_list[k]
            df_trace = df_pos.loc[df_pos['lineage']==trace]
            
            fig, ax = plt.subplots()
            #ax.plot(df_trace['frame'],c3_diff)
            ax.plot(df_trace['frame'],df_trace['Mean.Intensity.c2'],'r')
            ax.set_ylabel('circadian',color = 'r')
            ax2 = ax.twinx()
            ax2.plot(df_trace['frame'],df_trace['Mean.Intensity.c3'],'g')
            ax2.set_ylabel('Geminin',color = 'g')
            ax.set_title(str(pos)+'_'+str(trace))
            xline = list(df_trace.loc[df_trace['division'] == 1]['frame'])
            for i in xline:
                ax.axvline(x=i,color='k')
            pp.savefig()
            plt.clf()
pp.close()

# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})
def set_axis(ax,xlabel,ylabel):
    ax.set_ylabel(ylabel, fontsize='20')
    ax.set_xlabel(xlabel, fontsize='20')
    ax.tick_params(labelsize='16')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

# trace removed (115_276)
file_name = condition_dict[1]
df = pd.read_csv('condition_table_division/%s.csv'%file_name)
df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
df_plot = df.loc[df['traceId'] == '115_276']

fig, ax = plt.subplots(figsize=(6,3))
ax.plot(df_plot['frame']*0.5, df_plot['Size_in_pixels_0'])
xline = list(df_plot.loc[(df_plot['division'] == 1)]['frame']*0.5)
for i in xline:
    ax.axvline(x=i,color='k',linestyle='--')
xlabel = 'Time (hour)'
ylabel = 'Nucleus Size (pixel)'
set_axis(ax,xlabel,ylabel)



# trace removed (115_175)
file_name = condition_dict[1]
df = pd.read_csv('condition_table_division/%s.csv'%file_name)
df['traceId'] = df['position'].astype(str) + '_' + df['lineage'].astype(str)
df_plot = df.loc[df['traceId'] == '115_175']

fig, ax = plt.subplots(figsize=(6,3))
ax.plot(df_plot['frame']*0.5, df_plot['Size_in_pixels_0'])
xline = list(df_plot.loc[(df_plot['division'] == 1)]['frame']*0.5)
for i in xline:
    ax.axvline(x=i,color='k',linestyle='--')
xlabel = 'Time (hour)'
ylabel = 'Nucleus Size (pixel)'
set_axis(ax,xlabel,ylabel)
    
    
    