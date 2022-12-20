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


folder = '/Users/pieter/Documents/COMPASS_reserve/COMPASS/HPC_files/Output'
criterion = 'IC'
sd = 0.1
nreps = 1000

def plot3D(criterion = 'IC', ntrials = np.arange(80, 1000, 160),
               ireversal = 40, npp = np.arange(40, 201, 20),
           sd = 0.2, main_folder = folder, nreps = 100, tau = 0.75, typeIerror = 0.05):
    if criterion == 'IC':
        ess = [.1, .2]
        ES_text = ''
        title = "Pr("+"\u03C1"+"("+ "\u1FB6" + "," + "\u03B1" +")) >= {}) with nreps = {}".format(tau, nreps)
        tau = tau
    elif criterion == 'GD':
        ess = [.2, .5]
        title = "Pr(" + "\u1FB6" + "_g1 >" + "\u1FB6" + "_g2" + ") with p-value threshold = {} and nreps = {}".format(typeIerror, nreps)
    elif criterion == 'EC':
        ess = [.1, .3]
        title = "Pr("+"\u03C1"+"("+ "\u1FB6" + "," + "\u03B4" +")) with p-value threshold = {} and nreps = {}".format(typeIerror, nreps)
    else:
        print("incorrect criterion")
        sys.exit()
    plot_folder = os.path.join(main_folder, 'Figures')
    if not os.path.isdir(plot_folder): os.makedirs(plot_folder)

    fig, axes = plt.subplots(nrows = 1, ncols = 2)
    for i in range(len(ess)):
        if criterion =='IC':
            sd = ess[i]
        else:
            ES_text = '{}ES'.format(ess[i])
        trials_ppcombo = np.array(list(itertools.product(ntrials, npp)))
        Power_df = pd.DataFrame(columns = npp, index = ntrials, dtype = 'float64')
        for itrials, ipp in zip(trials_ppcombo[:, 0], trials_ppcombo[:, 1]):
            nreversals = int(itrials/ireversal-1)
            file = 'Stats{}{}SD{}{}T{}R{}N{}reps.npy'.format(criterion, sd, ES_text,
                                                         itrials, nreversals, ipp, nreps)

            T_values = np.load(os.path.join(main_folder, file))
            if criterion == 'GD':
                tau = stat.t.ppf(1-typeIerror, ipp-1)
                T_values = np.abs(T_values)
            elif criterion == 'EC':
                beta_distribution = stat.beta((ipp/2)-1, (ipp/2)-1, loc = -1, scale = 2)
                tau = -beta_distribution.ppf(typeIerror)

            power = np.mean(T_values >= tau)
            Power_df.loc[itrials, ipp] = float(power)

            Power_array = Power_df

        sns.heatmap(Power_array, vmin = 0, vmax = 1, ax = axes[i], cmap = "viridis", annot=True, fmt='.2f')
        fig.suptitle(title, fontweight = 'bold')
        axes[i].set_ylabel('trials', loc = 'top')
        axes[i].set_xlabel('participants', loc = 'right')
        if criterion == 'IC': axes[i].set_title('SD = {}'.format(sd))
        elif criterion == 'GD': axes[i].set_title('ES = {}, SD = {}'.format(ess[i], sd))
        elif criterion == 'EC': axes[i].set_title('ES = {}, SD = {}'.format(ess[i], sd))

        fig.set_size_inches((12, 6), forward=False)
        fig.tight_layout()
        fig.savefig(os.path.join(plot_folder, 'Heatmap{}_{}nreps.png'.format(criterion, nreps)))

    return Power_df




Power_df = plot3D(criterion = criterion, sd = sd, nreps = nreps, tau = 0.75)
