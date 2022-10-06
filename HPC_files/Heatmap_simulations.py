# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 21:09:09 2022

@author: maudb
"""

import os, itertools, sys
from matplotlib import pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats as stat


folder = r'C:\Users\maudb\Documents\GitHub\COMPASS\HPC_files\Output'
criterion = 'GD'
sd = 0.1
ES = 0.8

def plot3D(criterion = 'IC', ntrials = np.arange(80, 1000, 160), 
               ireversal = 40, npp = np.arange(30, 100, 20), 
           sd = 0.2, main_folder = folder, nreps = 100, tau = 0.75, typeIerror = 0.05, ES = 1):
    if criterion == 'IC': 
        ES_text = ''
        title = 'P(r(LRestim, LRtrue) >= {}) with nreps = {} '.format(tau, nreps)
        tau = tau
    elif criterion == 'GD': 
        ES_text = '{}ES'.format(ES)
        title = 'P(rejectH0|H0false) with alpha = {} and nreps = {}'.format(typeIerror, nreps)
    else: 
        print("incorrect criterion")
        sys.exit()
    plot_folder = os.path.join(main_folder, 'Figures')
    if not os.path.isdir(plot_folder): os.makedirs(plot_folder)
    
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    trials_ppcombo = np.array(list(itertools.product(ntrials, npp)))
    Power_df = pd.DataFrame(columns = npp, index = ntrials, dtype = 'float64')
    for itrials, ipp in zip(trials_ppcombo[:, 0], trials_ppcombo[:, 1]):
        nreversals = int(itrials/ireversal-1)
        file = 'Stats{}{}SD{}{}T{}R{}N{}reps.npy'.format(criterion, sd, ES_text, 
                                                         itrials, nreversals, ipp, nreps)
        tau = stat.t.ppf(1-typeIerror, ipp-1)
        T_values = -np.load(os.path.join(main_folder, file))
        # print(T_values)
        # print(tau)
        power = np.mean(T_values >= tau)
        Power_df.loc[itrials, ipp] = float(power)
        
        Power_array = Power_df
        
    sns.heatmap(Power_array, vmin = 0, vmax = 1, ax = axes, cmap = "viridis", annot=True, fmt='.2f')
    fig.suptitle(title, fontweight = 'bold')
    axes.set_ylabel('trials', loc = 'top')
    axes.set_xlabel('participants', loc = 'right')
    if criterion == 'IC': axes.set_title('SD = {}'.format(sd))
    elif criterion == 'GD': axes.set_title('ES = {}'.format(ES))
    
    fig.set_size_inches((8, 6), forward=False)
    fig.tight_layout()
    fig.savefig(os.path.join(plot_folder, 'Heatmap{}{}SD.png'.format(criterion, sd)))
    
    return Power_df
            

    

Power_df = plot3D(criterion = criterion, sd = sd, ES = ES)
        
    
