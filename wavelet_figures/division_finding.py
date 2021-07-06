# -*- coding: utf-8 -*-
"""
Created on Mon May 31 18:18:13 2021

@author: Williams
@email: williams8645@gmail.com
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

def create_division(x):
    #select a position
    df_pos = df.loc[df['position'] == x]
    trace_list = list(set(df_pos['lineage']))
    
    #create an empty dataframe
    df_pos_new = pd.DataFrame(columns = df.columns)
     
    #loop on the traces, create the tables and combine them with the initiated table
    for j in trace_list:
        print('j',j)
        trace = j
        df_trace = df_pos.loc[df_pos['lineage'] == trace]
        if len(df_trace)<100:
            continue
        
        #create a Series of differentiated Geminin signal
        c3_diff = list(df_trace.set_index('frame').diff()['Mean.Intensity.c3'])
        
        c3_diff.extend([0,0,0,0,0])
        division = []
        c=0
        #loop on differentiated Geminin signal, one is marked as division when it drops more than 1000
        #mark division as 1, no division as 0 in the list called 'division'
        #set a counter that only allows division to happen again after 24 frames, namely 12 hours
        for i in range(len(c3_diff)-5):
            if (c3_diff[i] < -1000) & (c == 0) & (c3_diff[i+1]<100) & (c3_diff[i+2]<100) & (c3_diff[i+3]<100) & (c3_diff[i+4]<100) & (c3_diff[i+5]<100):
                division.append(1)
                c=23
            else:
                division.append(0)
                if c != 0:
                    c-=1
        
        df_trace['division'] = division
        df_pos_new = df_pos_new.append(df_trace)
    
    #return a new table for this position
    return df_pos_new

#loop on different conditions
for k in condition_dict:
    file_name = condition_dict[k]
    df = pd.read_csv('./condition_table/%s.csv'%file_name)
    
    #create a position list to iterate on
    pos_list = list(set(df['position']))
    
    #create an empty dataframe
    df_new = pd.DataFrame(columns = df.columns)
    
    #iterate on different positions
    for l in pos_list:
        print('l',l)
        df_new = df_new.append(create_division(l))
        
    #save the table for each condition
    df_new.to_csv('./condition_table_division/%s.csv'%condition_dict[k],index = False)
    

#export plots to visualize the result.
#In each condition, I selected 2 positons, in each of which I further selected 3 traces to plot
from matplotlib.backends.backend_pdf import PdfPages

os.chdir('D:/Charite/labA/WP2/condition_table_division')

#opend a mutlipage pdf
pp = PdfPages('./Geminin_division.pdf')
for i in condition_dict:
    file_name = condition_dict[i]
    df = pd.read_csv('./%s.csv'%file_name)
    pos_list = list(set(df['position']))
    print(pos_list)
    
    for j in range(2):
        pos = pos_list[j]
        df_pos = df.loc[df['position'] == pos]
        trace_list = list(set(df_pos['lineage']))
        print(trace_list) 
        
        for k in range(3):
            trace = trace_list[k]
            df_trace = df_pos.loc[df_pos['lineage']==trace]
            
            fig, ax = plt.subplots()
            #ax.plot(df_trace['frame'],c3_diff)
            ax.plot(df_trace['frame'],df_trace['Mean.Intensity.c3'])
            xline = list(df_trace.loc[df_trace['division'] == 1]['frame'])
            for i in xline:
                ax.axvline(x=i,color='k')
            pp.savefig()
pp.close()







