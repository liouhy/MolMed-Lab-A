# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:38:32 2021

@author: William
@email: williams8645@gmail.com
"""

import h5py
import os 
from skimage import io, exposure
#from matplotlib import pyplot as plt

field = input('select a field (eg.xy001):')

dirname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirname)
os.chdir('../')

raw_path = 'E:/Microscopy/RAW_DATA002'

def merge(i):
    imc2 = io.imread('%s/%sc2t%03d.tif'%(raw_path,field,i+1))
    imc3 = io.imread('%s/%sc3t%03d.tif'%(raw_path,field,i+1))
    imc2_eq = exposure.equalize_hist(imc2)
    imc3_eq = exposure.equalize_hist(imc3)
    im_merge = imc2_eq*0.8+imc3_eq*0.2
    return im_merge

with h5py.File('./merge/%s.h5'%field,'a') as f:
    for i in range(232):
        im_merge = merge(i)
        f.create_dataset('t%03d/channel0'%i,data=im_merge)
 
#io.imshow(im_merge)
#plt.show()
#plt.hist(im.flatten(),256,[0,256], color = 'r')