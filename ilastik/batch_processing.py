# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:32:29 2021

@author: William
@email: williams8645@gmail.com
"""
import h5py
import os 
from skimage import io, exposure
import subprocess
import shutil
import numpy as np

field_list = np.arange(5,430,5).tolist()
x=np.arange(20,430,20).tolist()
for i in x:
    field_list.remove(i)

ilastik_location = 'C:/Program Files/ilastik-1.3.3post3'
os.chdir(ilastik_location)
raw_path = 'E:/Microscopy/2020/2020-07-08/RAW_DATA002'
ilppath = 'E:/ilp_files/'
outparentdir = 'E:/Output/'


def make_folders():
    try:
        os.mkdir('E:/temp')
    except Exception:
        pass
    
    try:
        os.mkdir('E:/temp/xy%03d'%field)
    except Exception:
        pass
    
    try:
        os.mkdir(outpath) 
    except Exception:
        pass


#make the adjusted image sequence
def merge(i):
    imc2 = io.imread('%s/xy%03dc2t%03d.tif'%(raw_path,field,i+1))
    imc3 = io.imread('%s/xy%03dc3t%03d.tif'%(raw_path,field,i+1))
    imc2_eq = exposure.equalize_hist(imc2)
    imc3_eq = exposure.equalize_hist(imc3)
    im_merge = imc2_eq*0.8+imc3_eq*0.2
    return im_merge


def run_ilastik():
    pixelclass= 'E:/temp/xy%03d/xy%03d-t_pixelclass.h5' % (field, field)
    tracking= 'E:/temp/xy%03d/xy%03d-t_tracking.h5' % (field, field)
    #run pixel classification
    command1 = '.\ilastik.exe --headless --project=%spixel_classification.ilp --export_source="probabilities" --output_filename_format="E:/temp/xy%03d/{nickname}_pixelclass.h5" --raw_data E:/temp/xy%03d/xy%03d.h5/*' % (ilppath, field, field, field) #bash command for pixel classification, Change the path of 'project' to the .ilp file
    print ("\n\n%s" % command1)
    subprocess.call(command1, shell=True)
    
    #run tracking
    command3 = '.\ilastik.exe --headless --project=%sLineagetracking.ilp --export_source="Plugin" --export_plugin="CSV-Table" --output_filename_format="%s/{nickname}_tracking_table" --raw_data E:/temp/xy%03d/xy%03d.h5/* --prediction_maps "%s"' % (ilppath, outpath, field, field, pixelclass) #bash command for tracking, Change the path of 'project' to the .ilp file
    print ("\n\n%s" % command3)
    subprocess.call(command3, shell=True)
    command4 = '.\ilastik.exe --headless --project=%sLineagetracking.ilp --export_source="Object-Identities" --output_filename_format="E:/temp/xy%03d/{nickname}_tracking.h5" --raw_data E:/temp/xy%03d/xy%03d.h5/* --prediction_maps "%s"' % (ilppath, field, field, field, pixelclass) #bash command for tracking, Change the path of 'project' to the .ilp file
    print ("\n\n%s" % command4)
    subprocess.call(command4, shell=True)
        
    #run intensity files
    command5 = 'ilastik.exe --headless --project=%sintensities_channel2_A.ilp --table_filename=%s/xy%03dchannel2intensities.csv --raw_data E:/temp/xy%03d/xy%03dc2.h5/* --segmentation_image "%s"' % (ilppath, outpath, field, field, field, tracking) #bash command for channel-2 intensities, Change the path of project to the .ilp file
    print ("\n\n%s" % command5)
    subprocess.call(command5, shell=True)
    
    command6 = 'ilastik.exe --headless --project=%sintensities_channel3_A.ilp --table_filename=%s/xy%03dchannel3intensities.csv --raw_data E:/temp/xy%03d/xy%03dc3.h5/* --segmentation_image "%s"' % (ilppath, outpath, field, field, field, tracking) #bash command for channel 3 intensities,  Change the path of project to the .ilp file
    print ("\n\n%s" % command6)
    subprocess.call(command6, shell=True)

error = ['0']

#start running
for field in field_list:
    try:
        outpath = os.path.join(outparentdir,'xy%03d'%field)

        #create folders
        make_folders()
        
        #make the adjusted image sequence
        with h5py.File('E:/temp/xy%03d/xy%03d.h5'% (field, field),'a') as f:
            for i in range(232):
                im_merge = merge(i)
                f.create_dataset('t%03d/channel0'%i,data=im_merge)
        
        #make the image sequences for both channels
        for channel in [2,3]:
            with h5py.File('E:/temp/xy%03d/xy%03dc%d.h5'%(field,field,channel),'a') as f:
                for i in range(232):
                    im = io.imread('%s/xy%03dc%dt%03d.tif'%(raw_path,field,channel,i+1))
                    f.create_dataset('t%03d/channel0'%i,data=im)
        
        #run ilastik
        run_ilastik()
        
        #delete temp folder
        shutil.rmtree('E:/temp/xy%03d'% field, ignore_errors=True)
    except:
        error.append('xy%03d'% field)
        continue
    
with open('E:/error_log.txt','w') as f:
    for i in error:
        f.write(i+'\n')













    