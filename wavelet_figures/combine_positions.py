# -*- coding: utf-8 -*-
"""
Created on Fri May 28 21:26:44 2021
combine tables for each condition, add their position in one column
@author: William
@email: williams8645@gmail.com
"""

import pandas as pd
import os
import numpy as np

dirname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirname)
os.chdir('../')
table_path = 'D:/Charite/labA/WP1/Large_scale_image_processing/Mydata/longtable'

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


