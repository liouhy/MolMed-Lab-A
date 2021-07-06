# -*- coding: utf-8 -*-
"""
Created on Wed Jun 2 10:42:30 2021

@author: William
@email: williams8645@gmail.com
"""

from pyboat import ensemble_measures as em
import os 
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

os.chdir('D:/Charite/labA/WP2')


condition_dict = {1:'high_density_untreated',2:'high_density_0uM',3:'high_density_1.25uM',
             4:'high_density_2.5uM',5:'high_density_5uM',6:'high_density_10uM',
             7:'medium_density_untreated',8:'medium_density_0uM',9:'medium_density_1.25uM',
             10:'medium_density_2.5uM',11:'medium_density_5uM',12:'medium_density_10uM',
             13:'low_density_untreated',14:'low_density_0uM',15:'low_density_1.25uM',
             16:'low_density_2.5uM',17:'low_density_5uM',18:'low_density_10uM',
             19:'very_low_density_untreated',20:'very_low_density_0uM',21:'very_low_density_1.25uM'}



# get ensemble dynamics  (with power selection)
for i in condition_dict:
    ridge_results = {}
    t = 10
    file_name = condition_dict[i]+'_circadian'
    powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
    powers_series.set_index('index',inplace=True)
    
    ridge_table = pd.read_csv('wider_table/ridge_result/%s.csv'%file_name)
    ridge_table.set_index('frame',inplace=True)
    traceId_list = list(set(ridge_table['traceId']))
    
    #create ridge_results dict
    for k in traceId_list:
        table = ridge_table.loc[ridge_table['traceId']==k]
        ridge_results[k] = table.drop(columns='traceId')
    
    select_index = powers_series.loc[powers_series['0']>10].index
    high_power_ridge_results = [ridge_results[i] for i in select_index]
    
    periods_mq1q3, amplitudes_mq1q3, powers_mq1q3, phases_R = em.get_ensemble_dynamics(high_power_ridge_results)
    
    periods_mq1q3.to_csv('wider_table/ED/%s_ED_periods_high_power.csv'%file_name)
    amplitudes_mq1q3.to_csv('wider_table/ED/%s_ED_amp_high_power.csv'%file_name)
    powers_mq1q3.to_csv('wider_table/ED/%s_ED_powers_high_power.csv'%file_name)
    phases_R.to_csv('wider_table/ED/%s_ED_phases_high_power.csv'%file_name)
    
    #pl.ensemble_dynamics(*res)
        

        
# get ensemble dynamics(no power selection)
for i in condition_dict:
    ridge_results = {}
    file_name = condition_dict[i]+'_circadian'
    powers_series = pd.read_csv('wider_table/powerseries/%s_powerseries.csv'%file_name)
    powers_series.set_index('index',inplace=True)
    
    ridge_table = pd.read_csv('wider_table/ridge_result/%s.csv'%file_name)
    ridge_table.set_index('frame',inplace=True)
    traceId_list = list(set(ridge_table['traceId']))
    
    #create ridge_results dict
    for k in traceId_list:
        table = ridge_table.loc[ridge_table['traceId']==k]
        ridge_results[k] = table.drop(columns='traceId')
    
    select_index = powers_series.loc[powers_series['0']>1].index # change here to set power threshold
    high_power_ridge_results = [ridge_results[i] for i in select_index]
    
    periods_mq1q3, amplitudes_mq1q3, powers_mq1q3, phases_R = em.get_ensemble_dynamics(high_power_ridge_results)
    
    periods_mq1q3.to_csv('wider_table/ED/%s_ED_periods.csv'%file_name)
    amplitudes_mq1q3.to_csv('wider_table/ED/%s_ED_amp.csv'%file_name)
    powers_mq1q3.to_csv('wider_table/ED/%s_ED_powers.csv'%file_name)
    phases_R.to_csv('wider_table/ED/%s_ED_phases.csv'%file_name)



# high power
# plot ensemble dynamic results (phase coherrence)

# reset the font style
plt.rcdefaults()
# set the font name for a font family
plt.rcParams.update({'font.sans-serif':'Arial Unicode MS'})

for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['red','orange','lime','cyan','b','orchid']
    label_list = ['untreated','DMSO','1.25'+r'$\mu$'+'M','2.5'+r'$\mu$'+'M',
                  '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
    fig, ax = plt.subplots(figsize=(6,3))
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        phases = pd.read_csv('wider_table/ED/%s_ED_phases_high_power.csv'%file_name)
        ax.plot(phases['frame']/2,phases['R'],color=color_list[j-1],label=label_list[j-1])
        
    #plt.xlim(10,110)
    ax.legend()
    ax.set_xlabel('Time (hour)',fontsize='20')
    ax.set_ylabel('Phase coherence',fontsize='20')
    ax.tick_params(labelsize='16')
    ax.set_title(title_list[int(i/6)], fontsize='25')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig('graph/%s_circadian_phase_coherence_high_power.png'%title_list[int(i/6)])


# exponantial curve fit
label_list = ['DMSO', '5'+r'$\mu$'+'M','10'+r'$\mu$'+'M']
color_list = ['orange','b','orchid']
delta_list = [30,20,5] # starting time to fit for DMSO, 5uM, 10uM
dict_num = [2,5,6]
fig, ax = plt.subplots(figsize=(6,3))
for i in range(3):
    delta = delta_list[i]
    file_name = condition_dict[dict_num[i]]+'_circadian_ED_phases_high_power'
    df = pd.read_csv('wider_table/ED/%s.csv' % file_name)
    
    def exp(b,x):
        a=df.iloc[delta*2]['R'] #Initial point of the phase coherence
        return a*np.exp(-b*x)
    
    name=label_list[i]
    time=df['frame']/2 # hour
    phases=df['R']
    time_vect=[]
    ph_coh=[]
    #Choosing only the necessary values of the phase coherence (starting from the maximum point)
    for j in range(len(df['frame'])-delta*2):
        time_vect.append(df.iloc[j][0])
        ph_coh.append(df.iloc[j+delta*2]['R'])

    time_vect=np.reshape(time_vect,len(time_vect))
    ph_coh=np.reshape(ph_coh,len(ph_coh))
    #a=df.iloc[delta][col]

    popt,pcov=curve_fit(exp,time_vect,ph_coh, [0.1]) #Function for fitting and giving an initial value for the parameter to fit
    print(name, popt)

    
    ax.plot(time, phases, color=color_list[i])
    ax.plot(time_vect/2+delta,ph_coh,label=str(name)+' decay rate: %.5f' % (popt[0]),
            color=color_list[i])

    ax.plot(time_vect/2+delta,exp(popt[0],time_vect),'--',color=color_list[i])

ax.legend()
ax.set_title('High density', fontsize='25')
ax.set_xlabel('Time (hour)', fontsize='20')
ax.set_ylabel('Phase coherence', fontsize='20')
ax.tick_params(labelsize='16')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)





# plot ensemble dynamic results (periods)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        periods = pd.read_csv('wider_table/ED/%s_ED_periods_high_power.csv'%file_name)
        ax.plot(periods['frame']/2,periods['median'],color=color_list[j-1],label=label_list[j-1])
        #ax.fill_between(periods['frame']/2, periods["Q1"], periods["Q3"], color=color_list[j-1], alpha=0.3)
        
    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Periods (hour)')
    ax.set_title(title_list[int(i/6)]+' '+'power > 10')
   
    plt.savefig('graph/%s_circadian_periods_high_power.png'%title_list[int(i/6)])
    

# plot ensemble dynamic results (amplitudes)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        amplitudes = pd.read_csv('wider_table/ED/%s_ED_amp_high_power.csv'%file_name)
        ax.plot(amplitudes['frame']/2,amplitudes['median'],color=color_list[j-1],label=label_list[j-1])
               
    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Amplitudes (a.u.)')
    ax.set_title(title_list[int(i/6)]+' '+'power > 10')
    plt.savefig('graph/%s_circadian_amp_high_power.png'%title_list[int(i/6)])



# plot ensemble dynamic results (powers)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
     
        powers = pd.read_csv('wider_table/ED/%s_ED_powers_high_power.csv'%file_name)
        ax.plot(powers['frame']/2,powers['median'],color=color_list[j-1],label=label_list[j-1])

    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Powers (a.u.)')
    ax.set_title(title_list[int(i/6)]+' '+'power > 10')
    plt.savefig('graph/%s_circadian_powers_high_power.png'%title_list[int(i/6)])






# no power selection
# plot ensemble dynamic results (phase coherrence)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        phases = pd.read_csv('wider_table/ED/%s_ED_phases.csv'%file_name)
        ax.plot(phases['frame']/2,phases['R'],color=color_list[j-1],label=label_list[j-1])
        
    #plt.xlim(10,110)
    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Phase coherence')
    ax.set_title(title_list[int(i/6)])
    plt.savefig('graph/%s_circadian_phase_coherence.png'%title_list[int(i/6)])



# plot ensemble dynamic results (periods)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        periods = pd.read_csv('wider_table/ED/%s_ED_periods.csv'%file_name)
        ax.plot(periods['frame']/2,periods['median'],color=color_list[j-1],label=label_list[j-1])
        #ax.fill_between(periods['frame']/2, periods["Q1"], periods["Q3"], color=color_list[j-1], alpha=0.3)
        
    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Periods (hour)')
    ax.set_title(title_list[int(i/6)])
   
    plt.savefig('graph/%s_circadian_periods.png'%title_list[int(i/6)])
    

# plot ensemble dynamic results (amplitudes)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
        
        amplitudes = pd.read_csv('wider_table/ED/%s_ED_amp.csv'%file_name)
        ax.plot(amplitudes['frame']/2,amplitudes['median'],color=color_list[j-1],label=label_list[j-1])
               
    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Amplitudes (a.u.)')
    ax.set_title(title_list[int(i/6)])
    plt.savefig('graph/%s_circadian_amp.png'%title_list[int(i/6)])



# plot ensemble dynamic results (powers)
for i in [0,6,12]:
    title_list = ['High density','Medium density',"Low density"]
    color_list = ['tomato','orange','lime','cyan','b','orchid']
    label_list = ['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
    fig, ax = plt.subplots()
    for j in [1,2,3,4,5,6]:
        file_name = condition_dict[i+j]+'_circadian'
     
        powers = pd.read_csv('wider_table/ED/%s_ED_powers.csv'%file_name)
        ax.plot(powers['frame']/2,powers['median'],color=color_list[j-1],label=label_list[j-1])

    ax.legend()
    ax.set_xlabel('Time (hour)')
    ax.set_ylabel('Powers (a.u.)')
    ax.set_title(title_list[int(i/6)])
    plt.savefig('graph/%s_circadian_powers.png'%title_list[int(i/6)])