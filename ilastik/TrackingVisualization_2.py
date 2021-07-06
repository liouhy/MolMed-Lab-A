# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:42:15 2021

@author: Huai-Yu William Liou
@email: williams8645@gmail.com
"""
import os
from PIL import Image, ImageDraw
import imageio
import numpy as np
import cv2
from skimage import io, exposure
import random

field = input('select a field (eg.xy001):')
#set working directory to the path of this script
dirname = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirname)
os.chdir('../')
raw_path = 'E:/Microscopy/RAW_DATA002'

#open the csv file
import pandas as pd
data = pd.read_csv('longtable/%s_final_table.csv'%field,
                   usecols=('frame','lineageId','xcenter','ycenter','lineage'))
li = set(data['lineageId'])
li_color = {}
for i in li:
    li_color[i] = (random.randint(0,254),random.randint(0,254),random.randint(0,254))

#draw squares and lineageId
with imageio.get_writer('video/%s.mp4'%field, format='mp4', mode='I', fps=10) as writer:#write images into a mp4
    for i in range(232):
        #pre-process the images
        imc2 = io.imread('%s/%sc2t%03d.tif'%(raw_path,field,i+1))
        imc3 = io.imread('%s/%sc3t%03d.tif'%(raw_path,field,i+1))
        imc2_eq = exposure.equalize_hist(imc2)
        imc3_eq = exposure.equalize_hist(imc3)
        im_merge = imc2_eq*0.8+imc3_eq*0.2
        #change to unit8 format, then RGB
        array = np.uint8(im_merge*255)
        color = cv2.cvtColor(array,cv2.COLOR_GRAY2RGB)
        im = Image.fromarray(color) #read the array into PIL image
        draw = ImageDraw.Draw(im)
        for l in li:
            selectdf=data[data['lineageId']==l]
            selectdf=selectdf[selectdf['frame']==i]
            for j in range(len(selectdf.index)):
               selectdf=selectdf.iloc[j]
               x=int(selectdf['xcenter'])
               y=int(selectdf['ycenter'])
               c=li_color[l]
               draw.rectangle((x-5,y-5,x+5,y+5), fill = c)
               draw.text((x,y), str(selectdf.iloc[1]), fill = (0,0,0))
               draw.rectangle((0,0,20,10), fill = (254,254,254))
               draw.text((0,0),str(selectdf.iloc[0]), fill = (0,0,0))
               selectdf=data[data['lineageId']==l]
               selectdf=selectdf[selectdf['frame']==i]
        writer.append_data(np.asarray(im))



