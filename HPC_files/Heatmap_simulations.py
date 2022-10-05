# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 21:09:09 2022

@author: maudb
"""

import os, itertools
from matplotlib import pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns

tau = 0.75
folder = r'C:\Users\maudb\Documents\GitHub\COMPASS\HPC_files\Output'




def plot3D(criterion = 'IC', ntrials = np.arange(80, 1000, 160), 
               ireversal = 40, npp = np.arange(30, 100, 20), 
           sd = 0.2, main_folder = folder, nreps = 100, tau = 0.75):
    plot_folder = os.path.join(main_folder, 'Figures')
    if not os.path.isdir(plot_folder): os.makedirs(plot_folder)
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    trials_ppcombo = np.array(list(itertools.product(ntrials, npp)))
    Power_df = pd.DataFrame(columns = npp, index = ntrials, dtype = 'float64')
    for itrials, ipp in zip(trials_ppcombo[:, 0], trials_ppcombo[:, 1]):
        nreversals = int(itrials/ireversal-1)
        file = 'Stats{}{}SD{}T{}R{}N{}reps.npy'.format(criterion, sd, itrials, nreversals, ipp, nreps)
        power = np.mean(np.load(os.path.join(main_folder, file)) >= tau)
        Power_df.loc[itrials, ipp] = float(power)
        
        Power_array = Power_df
        
    sns.heatmap(Power_array, vmin = 0, vmax = 1, ax = axes, cmap = "viridis", annot=True, fmt='.2f')
    title = 'P(r(LRestim, LRtrue) >= {}) with nreps = {} '.format(tau, nreps)
    fig.suptitle(title, fontweight = 'bold')
    axes.set_ylabel('trials', loc = 'top')
    axes.set_xlabel('participants', loc = 'right')
    axes.set_title('SD = {}'.format(sd))
    
    fig.set_size_inches((8, 6), forward=False)
    fig.tight_layout()
    fig.savefig(os.path.join(plot_folder, 'Heatmap{}{}SD.png'.format(criterion, sd)))
    
    return Power_df
            

    

Power_df = plot3D()
        
    
