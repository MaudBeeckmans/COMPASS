# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:59:30 2022

@author: maudb
"""

import os, itertools, sys
import numpy as np

def combine_output(criterion = 'IC', variable = 'Statistic', ntrials = np.array([80]), ireversal = 40, 
                   npp = np.array([60]), sd = 0.2, main_folder = os.getcwd(), 
                   nreps = 100):
    
    trials_ppcombo = np.array(list(itertools.product(ntrials, npp)))
    read_folder = os.path.join(main_folder, 'Output')
    for itrials, ipp in zip(trials_ppcombo[:, 0], trials_ppcombo[:, 1]):
    
        nreversals = int(itrials/ireversal-1)
        
        folder = os.path.join(read_folder, 'Results{}{}SD{}T{}R{}N'.format(criterion, sd, itrials, nreversals, ipp))
        Stats = np.array([])
        for irep in range(1, nreps+1):
            
            Statistic = np.load(os.path.join(folder, "{}_rep{}.npy".format(variable, irep)))
            Stats = np.append(Stats, Statistic)
        np.save(os.path.join(main_folder, 'Stats{}{}SD{}T{}R{}N{}reps.npy'.format(criterion, sd, itrials, nreversals, ipp, nreps)), Stats)
    

input_parameters = sys.argv[1:]
assert len(input_parameters) == 2
criterion = input_parameters[0]
SD = input_parameters[1]


combine_output(criterion = criterion, variable = 'Statistic', ntrials = np.arange(80, 1000, 160), 
               ireversal = 40, npp = np.arange(30, 100, 20), sd = SD, 
               main_folder = r'/user/data/gent/442/vsc44254/COMPASS/Version2022_2023', 
               nreps = 100)
        
        
        
    