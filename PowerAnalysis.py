# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:04:23 2021

@author: maudb
"""

import numpy as np
import pandas as pd 
from multiprocessing import Pool, cpu_count
from Functions import create_design, correlation_repetition, groupdifference_repetition, check_input_parameters
from scipy import optimize
from statsmodels.stats.power import tt_ind_solve_power
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def power_estimation_correlation(npp = 30, ntrials = 480, nreversals = 12, cut_off = 0.7, high_performance = False, 
                                 nreps = 100, reward_probability = 0.8, mean_LRdistribution = 0.5, SD_LRdistribution = 0.1, 
                                 mean_inverseTempdistribution = 2.0, SD_inverseTempdistribution = 1.0): 
    """

    Parameters
    ----------
    npp : integer
        Number of participants in the study.
    ntrials : integer
        Number of trials that will be used to do the parameter recovery analysis for each participant.
    nreps : integer
        Number of repetitions that will be used for the parameter estimation process. 
    cut_off : float
        Critical value that will be used to evaluate whether the repetition was successful. 
    high_performance : bool (True or False)
        Defines whether multiple cores on the computer will be used in order to estimate the power. 
    nreversals : integer
        The number of rule-reversals that will occur in the experiment. Should be smaller than ntrials.
    reward_probability : float (element within [0, 1]), optional
        The probability that reward will be congruent with the current stimulus-response mapping rule. The default is 0.8.

    Returns
    -------
    allreps_output : TYPE
        Pandas dataframe containing the proportion failed estimates on each repetition and the correlation value on each repetition.
    power_estimate: float [0, 1]
        The power estimation: number of reps for which the parameter recovery was successful (correlation > significance_cutoff) divided by the total number of reps. 
    
    Description
    -----------
    Function that actually calculates the power to obtain adequate parameter estimates. 
    Parameter estimates are considered to be adequate if their correlation with the true parameters is minimum the cut_off.
    Power is calculated using a simulation-based approach.
    """
    start_design = create_design(ntrials = ntrials, nreversals = nreversals, reward_probability = reward_probability)
    if high_performance == True: n_cpu = cpu_count() - 2
    else: n_cpu = 1
    pool = Pool(processes = n_cpu)
    LR_distribution = np.array([mean_LRdistribution, SD_LRdistribution])
    inverseTemp_distribution = np.array([mean_inverseTempdistribution, SD_inverseTempdistribution])
    out = pool.starmap(correlation_repetition, [(inverseTemp_distribution, LR_distribution, npp, ntrials, 
                                                 start_design, rep, nreps, n_cpu) for rep in range(nreps)])
    pool.close()
    pool.join()
    
    # allreps_output = pd.DataFrame(out, columns = ['propfailed_estimates', 'correlations'])
    # mean_propfailed_estimates = np.mean(allreps_output['propfailed_estimates'])
    
    allreps_output = pd.DataFrame(out, columns = ['correlations'])
    
    
    power_estimate = np.mean((allreps_output['correlations'] >= cut_off)*1)
    print(str("\nPower to obtain a correlation(true_param, param_estim) >= {}".format(cut_off) 
          + " with {} trials and {} participants: {}%".format(ntrials, npp, power_estimate*100)))
    # print("\nMean failed learning rate estimates: {}%".format(np.round(mean_propfailed_estimates*100, 2)))
    return allreps_output, power_estimate

def power_estimation_groupdifference(npp_per_group = 20, ntrials = 480, nreps = 100, cut_off = 0.05, 
                                     high_performance = False, nreversals = 12, reward_probability = 0.8, 
                                     mean_LRdistributionG1 = 0.5, SD_LRdistributionG1 = 0.1, 
                                     mean_LRdistributionG2 = 0.5, SD_LRdistributionG2 = 0.1, 
                                     mean_inverseTempdistributionG1 = 2.0, SD_inverseTempdistributionG1 = 1.0, 
                                     mean_inverseTempdistributionG2 = 2.0, SD_inverseTempdistributionG2 = 1.0): 
    """
    Parameters
    ----------
    npp_per_group : integer
        Number of participants per group in the study.
    ntrials : integer
        Number of trials that will be used to do the parameter recovery analysis for each participant.
    nreps : integer
        Number of repetitions that will be used for the parameter estimation process. 
    cut_off : float
        Critical value that will be used to evaluate whether the repetition was successful. 
    high_performance : bool (True or False)
        Defines whether multiple cores on the computer will be used in order to estimate the power. 
    nreversals : integer
        The number of rule-reversals that will occur in the experiment. Should be smaller than ntrials.
    reward_probability : float (element within [0, 1]), optional
        The probability that reward will be congruent with the current stimulus-response mapping rule. The default is 0.8.

    Returns
    -------
    allreps_output : TYPE
        Pandas dataframe containing the proportion failed estimates on each repetition and the p-value on each repetition.
    power_estimate: float [0, 1]
        The power estimation: number of reps for which the parameter recovery was successful (significant group difference found) divided by the total number of reps. 
    
    Description
    -----------
    Function that actually calculates the power to obtain adequate parameter estimates. 
    Parameter estimates are considered to be adequate if they correctly reveal the group difference when a true group difference of size 'cohens_d' exists.
    Power is calculated using a simulation-based approach.
    """
    
    start_design = create_design(ntrials = ntrials, nreversals = nreversals, reward_probability = reward_probability)
    if high_performance == True: n_cpu = cpu_count() - 2
    else: n_cpu = 1
    if __name__ == '__main__': 
        # First: check what the power is when true parameters would be recoverable 
        power = tt_ind_solve_power(nobs1 = npp_per_group, ratio = 1, effect_size = cohens_d, alpha = cut_off, power = None, 
                                alternative = 'larger')
        print("\nPower if estimates would be perfect: {}%".format(np.round(power, 4)*100))    
        
        
        
        LR_distributions = np.array([[mean_LRdistributionG1, SD_LRdistributionG1], [mean_LRdistributionG2, SD_LRdistributionG2]])
        inverseTemp_distributions = np.array([[mean_inverseTempdistributionG1, SD_inverseTempdistributionG1], 
                                              [mean_inverseTempdistributionG2, SD_inverseTempdistributionG2]])
        
        
        pool = Pool(processes = n_cpu)
        out = pool.starmap(groupdifference_repetition, [(inverseTemp_distributions, LR_distributions, npp_per_group, 
                                                     ntrials, start_design, rep, nreps, n_cpu, False) for rep in range(nreps)])
        # before calling pool.join(), should call pool.close() to indicate that there will be no new processing
        pool.close()
        pool.join()
        # allreps_output = pd.DataFrame(out, columns = ['propfailed_estimates', 'p_values'])
        allreps_output = pd.DataFrame(out, columns = ['p_values'])
        
        # check for which % of repetitions the group difference was significant 
        # note that we're working with a one-sided t-test (if interested in two-sided need to divide the p-value obtained at each rep with 2)
        power_estimate = np.mean((allreps_output['p_values'] <= cut_off))
        print(str("\nPower to detect a significant group difference when the estimated effect size d = {}".format(cohens_d)
              + " with {} trials and {} participants per group: {}%".format(ntrials, 
                                                                         npp_per_group, power_estimate*100)))
        # print("\nMean failed learning rate estimates per repetition: {}%".format(np.round(mean_propfailed_estimates*100, 2)))
        return allreps_output, power_estimate

#%%


import os, sys 

if __name__ == '__main__': 
    criterion = sys.argv[1:]
    assert len(criterion) == 1
    criterion = criterion[0]
    
    InputFile_name = "InputFile_{}.csv".format(criterion)
    InputFile_path = os.path.join(os.getcwd(), InputFile_name)
    InputParameters = pd.read_csv(InputFile_path, delimiter = ';')
    InputDictionary = InputParameters.to_dict()
    print(InputDictionary)
    
    # variables_fine = check_input_parameters(ntrials, nreversals, npp, reward_probability, full_speed, criterion, significance_cutoff, cohens_d, nreps, plot_folder)
    # if variables_fine == 0: break 
    # # should implement all the errors!
    # print("Power estimation for row {} in the input_file has begun, time for coffee whilst waiting :).".format(i))
    
    
    for row in range(InputParameters.shape[0]): 
        #Calculate how long it takes to do a power estimation 
        start_time = datetime.now()
        print("Power estimation started at {}.".format(start_time))
        
        #Extract all values that are the same regardless of the criterion used 
        ntrials = InputDictionary['ntrials'][row]
        nreversals = InputDictionary['nreversals'][row]
        reward_probability = InputDictionary['reward_probability'][row]
        nreps = InputDictionary['nreps'][row]
        full_speed = InputDictionary['full_speed'][row]
        output_folder = InputDictionary['output_folder'][row]
        
        if criterion == "IC":
            npp = InputDictionary['npp'][row]
            meanLR, sdLR = InputDictionary['meanLR'][row], InputDictionary['sdLR'][row]
            meanInverseT, sdInverseT = InputDictionary['meanInverseTemperature'][row], InputDictionary['sdInverseTemperature'][row]
            tau = InputDictionary['tau'][row]
            
            output, power_estimate = power_estimation_correlation(npp = npp, ntrials = ntrials, nreps = nreps, 
                                                                  cut_off = tau, 
                                               high_performance = full_speed, nreversals = nreversals, 
                                               reward_probability = reward_probability, mean_LRdistribution = meanLR, 
                                               SD_LRdistribution = sdLR, mean_inverseTempdistribution = meanInverseT, 
                                               SD_inverseTempdistribution = sdInverseT)
            fig, axes = plt.subplots(nrows = 1, ncols = 1)
            sns.kdeplot(output["correlations"], label = "correlations", ax = axes)
            fig.suptitle("P(correlation >= {} with {} pp, {} trials)".format(tau, npp, ntrials), fontweight = 'bold')
            axes.set_title("Power = {}% based on {} reps".format(np.round(power_estimate*100, 2), nreps))
            axes.axvline(x = tau, lw = 2, linestyle ="dashed", color ='k', label ='tau')
            
        elif criterion == "GD": 
            npp_pergroup = InputDictionary['npp_group'][row]
            meanLR_g1, sdLR_g1 = InputDictionary['meanLR_g1'][row], InputDictionary['sdLR_g1'][row]
            meanLR_g2, sdLR_g2 = InputDictionary['meanLR_g2'][row], InputDictionary['sdLR_g2'][row]
            meanInverseT_g1, sdInverseT_g1 = InputDictionary['meanInverseTemperature_g1'][row], InputDictionary['sdInverseTemperature_g1'][row]
            meanInverseT_g2, sdInverseT_g2 = InputDictionary['meanInverseTemperature_g2'][row], InputDictionary['sdInverseTemperature_g2'][row]
            typeIerror = InputDictionary['TypeIerror'][row]
            
            cohens_d = np.abs(meanLR_g1-meanLR_g2)/np.sqrt((sdLR_g1**2+sdLR_g2**2)/2)
            
            
            output, power_estimate = power_estimation_groupdifference(npp_per_group = npp_pergroup, ntrials = ntrials, 
                                               nreps = nreps, cut_off = typeIerror, high_performance = full_speed, 
                                               nreversals = nreversals, reward_probability = reward_probability, 
                                               mean_LRdistributionG1 = meanLR_g1, SD_LRdistributionG1 = sdLR_g1, 
                                               mean_LRdistributionG2 = meanLR_g2, SD_LRdistributionG2=sdLR_g2, 
                                               mean_inverseTempdistributionG1 = meanInverseT_g1, SD_inverseTempdistributionG1 = sdInverseT_g1, 
                                               mean_inverseTempdistributionG2 = meanInverseT_g2, SD_inverseTempdistributionG2 = sdInverseT_g2)
            fig, axes = plt.subplots(nrows = 1, ncols = 1)
            sns.kdeplot(output["p_values"], label = "p_values", ax = axes)
            fig.suptitle("P(p-value <= {}) with {} pp, {} trials".format(typeIerror, npp_pergroup, ntrials), fontweight = 'bold')
            axes.set_title("Power = {}% based on {} reps with ES = {}".format(np.round(power_estimate*100, 2), nreps, cohens_d))
            axes.axvline(x = typeIerror, lw = 2, linestyle ="dashed", color ='k', label ='typeIerror')
        
        else: print("Criterion not found")
        #final adaptations to the output figure & store the figure 
        fig.legend(loc = 'center right')
        fig.tight_layout()
        fig.savefig(os.path.join(output_folder, 'Distributionplot_{}_line{}.jpg'.format(criterion, row)))
        
        # measure how long the power estimation lasted 
        end_time = datetime.now()
        print("\nPower analysis ended at {}; run lasted {} hours.".format(end_time, end_time-start_time))
        