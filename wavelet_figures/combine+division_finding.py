# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 08:51:29 2021

@author: liouhy
"""

import pandas as pd
import os
import numpy as np


os.chdir('E:/')
table_path = 'E:/longtable'
"""
condition_combine_dict = {101:'high_density_untreated',81:'high_density_0uM',61:'high_density_1.25uM',
             41:'high_density_2.5uM',21:'high_density_5uM',1:'high_density_10uM',
             121:'medium_density_untreated',141:'medium_density_0uM',161:'medium_density_1.25uM',
             181:'medium_density_2.5uM',201:'medium_density_5uM',221:'medium_density_10uM',
             341:'low_density_untreated',321:'low_density_0uM',301:'low_density_1.25uM',
             281:'low_density_2.5uM',261:'low_density_5uM',241:'low_density_10uM',
             361:'very_low_density_untreated',381:'very_low_density_0uM',401:'very_low_density_1.25uM'}
f = [1,21,41,61,81,101,121,141,161,181,201,221,241,261,281,301,321,341,361,381,401]
for j in f:
    field = j
    #loop 1-20
    df = pd.read_csv('%s/xy%03d_final_table.csv'% (table_path, field))
    df['position'] = field
    df_final = df
    
    field = np.arange(j+1,j+20,1)
    for i in field:
        print(i)
        df = pd.read_csv('%s/xy%03d_final_table.csv'% (table_path, i))
        df['position'] = i 
        df_final = df_final.append(df)
    
    print('saving the table...')
    df_final.to_csv('./condition_table/%s.csv'%condition_combine_dict[j],index = False)
 """   
condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

def create_division(x):
    df_pos = df.loc[df['position'] == x]
    trace_list = list(set(df_pos['lineage']))
    
    trace = trace_list[0]
    
    df_trace = df_pos.loc[df_pos['lineage'] == trace]
    
    #create a Series of diffirentiated Geminin sigal
    c3_diff = list(df_trace.set_index('frame').diff()['Mean.Intensity.c3'])
    
    division = []
    c=0
    for i in c3_diff:
        if (i < -1000) & (c == 0):
            division.append(1)
            c=23
        else:
            division.append(0)
            if c != 0:
                c-=1
    df_trace['division'] = division
    df_pos_new = df_trace
    
    trace_list.remove(trace_list[0])
    for j in trace_list:
        trace = j
        df_trace = df_pos.loc[df_pos['lineage'] == trace]
        
        #create a Series of diffirentiated Geminin sigal
        c3_diff = list(df_trace.set_index('frame').diff()['Mean.Intensity.c3'])
        
        division = []
        c=0
        for i in c3_diff:
            if (i < -1000) & (c == 0):
                division.append(1)
                c=23
            else:
                division.append(0)
                if c != 0:
                    c-=1
        df_trace['division'] = division
        df_pos_new = df_pos_new.append(df_trace)
    return df_pos_new

for k in condition_dict:
    file_name = condition_dict[k]
    df = pd.read_csv('./condition_table/%s.csv'%file_name)
    
    #select a position
    pos_list = list(set(df['position']))
    pos = pos_list[0]
    df_new = create_division(pos)
    pos_list.remove(pos_list[0])
    for l in pos_list:
        df_new = df_new.append(create_division(l))
    df_new.to_csv('./condition_table_division/%s.csv'%condition_dict[k],index = False)
