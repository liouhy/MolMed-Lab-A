# -*- coding: utf-8 -*-
"""
Created on Wed Jun 2 10:42:30 2021

@author: William
@email: williams8645@gmail.com
"""

import numpy as np
from pyboat import WAnalyzer
from pyboat import ensemble_measures as em
#import matplotlib.pyplot as plt
import os 
import pandas as pd

os.chdir('D:/Charite/labA/WP2')


condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}

# create tables with ridge results for the cell cycle
for j in condition_dict:
    file_name = condition_dict[j]+'_cell_cycle'
         
    df = pd.read_csv('wider_table/%s.csv'% file_name)
    df.set_index('frame', inplace = True)
    
    
    # detrend and amplitude normalize the signals
    dt = 0.5
    p = np.linspace(10,40,400)
                
    wAn = WAnalyzer(p, dt)
       
    
    ridge_results = {} # get the the individual ridge readouts
    ridge_table = pd.DataFrame()
    
    # get the powers
    for i in df:
        signal = df[i].dropna()
        wAn.compute_spectrum(signal, do_plot = False) #False to not show each spectrum plot
        rd = wAn.get_maxRidge(power_thresh = 0, smoothing_wsize = 5)
        
        # give back the frame informaiton by index
        rd.set_index(signal.index,inplace=True)
        
        ridge_results[i] = rd
        rd['traceId'] = i
        ridge_table = ridge_table.append(rd)
    
    ridge_table = ridge_table.reset_index()
    ridge_table.to_csv('wider_table/ridge_result/%s.csv' % file_name, index=False)