# -*- coding: utf-8 -*-
"""
Created on Wed Jun 2 10:42:30 2021

@author: William
@email: williams8645@gmail.com
"""

import numpy as np
import os 
import pandas as pd
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

# plot histograms of circadian powers
for i in condition_dict:
    file_name = condition_dict[i]+'_circadian_powerseries'
    powers_series = pd.read_csv('wider_table/powerseries/%s.csv'% file_name)
    
    # plot the histogram
    kde = stats.gaussian_kde(powers_series['0'])
    fig, ax = plt.subplots()
    n,bins,patches=ax.hist(
        powers_series['0'],
        bins=np.arange(min(powers_series['0']),max(powers_series['0']),2),
        edgecolor='w',
        density=True)
    ax.plot(bins,kde(bins))
    ax.set_xlim((0,60))
    ax.set_xlabel('Average Ridge Power')
    ax.set_ylabel('Density')
    ax.set_title(condition_dict[i].capitalize()+' '+'n = %d' % len(powers_series))
    plt.savefig('./graph/%s.png' % file_name)
    plt.clf()