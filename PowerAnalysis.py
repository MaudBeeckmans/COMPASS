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
                                 nreps = 100, reward_probability = 0.8): 
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
    LR_distribution = np.array([0.5, 0.1])
    inverseTemp_distribution = np.array([2.0, 1.0])
    out = pool.starmap(correlation_repetition, [(inverseTemp_distribution, LR_distribution, npp, ntrials, 
                                                 start_design, rep, nreps, n_cpu) for rep in range(nreps)])
    pool.close()
    pool.join()
    
    allreps_output = pd.DataFrame(out, columns = ['propfailed_estimates', 'correlations'])
    mean_propfailed_estimates = np.mean(allreps_output['propfailed_estimates'])
    power_estimate = np.mean((allreps_output['correlations'] >= cut_off)*1)
    print(str("\nPower to obtain a correlation(true_param, param_estim) >= {}".format(cut_off) 
          + " with {} trials and {} participants: {}%".format(ntrials, npp, power_estimate*100)))
    print("\nMean failed learning rate estimates: {}%".format(np.round(mean_propfailed_estimates*100, 2)))
    return allreps_output, power_estimate

def power_estimation_groupdifference(npp_per_group = 20, ntrials = 480, nreps = 100, cut_off = 0.05, 
                                     high_performance = False, nreversals = 12, cohens_d = 0.5, reward_probability = 0.8): 
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
    cohens_d : float 
        Estimated effect size included in the power analysis. 
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
        
        # Calculate the mean_groupdifference based on cohens_d and with the s_pooled == 0.1
            # formula: cohens_d = (mean1 - mean2)/s_pooled ==> cohens_d * s_pooled = (mean1 - mean2)
            # thus with s_pooled == 0.1: cohens_d * 0.1 = group_difference
        s_pooled = 0.1
        group_difference = cohens_d * s_pooled 
        LR_means = [0.5 - group_difference/2, 0.5 + group_difference/2]
        LR_distributions = np.array([[LR_means[0], 0.1], [LR_means[1], 0.1]])
        
        inverseTemp_distribution = np.array([2.0, 1.0])
        # mean and standard deviation for the true distributions that will be used: 
            # assumed distribution learning rates: normal distribution with mean 0.5 and sd 0.1
            # assumed distribution inverse temperatures: normal distribution with mean 2 and sd 1
        pool = Pool(processes = n_cpu)
        out = pool.starmap(groupdifference_repetition, [(inverseTemp_distribution, LR_distributions, npp_per_group, 
                                                     ntrials, start_design, rep, nreps, n_cpu, False) for rep in range(nreps)])
        # before calling pool.join(), should call pool.close() to indicate that there will be no new processing
        pool.close()
        pool.join()
        allreps_output = pd.DataFrame(out, columns = ['propfailed_estimates', 'p_values'])
        mean_propfailed_estimates = np.mean(allreps_output['propfailed_estimates'])
        # check for which % of repetitions the group difference was significant 
        # note that we're working with a one-sided t-test (if interested in two-sided need to divide the p-value obtained at each rep with 2)
        power_estimate = np.mean((allreps_output['p_values'] <= cut_off))
        print(str("\nPower to detect a significant group difference when the estimated effect size d = {}".format(cohens_d)
              + " with {} trials and {} participants per group: {}%".format(ntrials, 
                                                                         npp_per_group, power_estimate*100)))
        print("\nMean failed learning rate estimates per repetition: {}%".format(np.round(mean_propfailed_estimates*100, 2)))
        return allreps_output, power_estimate

#%%


import os 

if __name__ == '__main__': 
    start_time = datetime.now()
    
    print("Power analysis started at {}.".format(start_time))
    
    parameter_file = pd.read_csv(os.path.join(os.getcwd(), "Input_file.csv"), delimiter = ';')
    
    for i in range(parameter_file.shape[0]):
        ntrials, nreversals, npp, reward_probability, full_speed, criterion, significance_cutoff, cohens_d, nreps, plot_folder  = parameter_file.loc[i, :]
        variables_fine = check_input_parameters(ntrials, nreversals, npp, reward_probability, full_speed, criterion, significance_cutoff, cohens_d, nreps, plot_folder)
        if variables_fine == 0: break 
        # should implement all the errors!
        print("Power estimation for row {} in the input_file has begun, time for coffee whilst waiting :).".format(i))
        if parameter_file.loc[i, 'criterion'] == "correlation": 
            output, power_estimate = power_estimation_correlation(npp = npp, ntrials = ntrials, nreps = nreps, cut_off = significance_cutoff, 
                                               high_performance = full_speed, nreversals = nreversals, 
                                               reward_probability = reward_probability)
            fig, axes = plt.subplots(nrows = 1, ncols = 1)
            sns.kdeplot(output["correlations"], label = "correlations", ax = axes)
            fig.suptitle("P(correlation >= {} with {} pp, {} trials)".format(significance_cutoff, npp, ntrials), fontweight = 'bold')
            axes.set_title("Power = {}% based on {} reps".format(np.round(power_estimate*100, 2), nreps))
        elif parameter_file.loc[i, 'criterion'] == "group_difference": 
            output, power_estimate = power_estimation_groupdifference(npp_per_group = npp, ntrials = ntrials, 
                                               nreps = nreps, cut_off = significance_cutoff, high_performance = full_speed, 
                                               nreversals = nreversals, cohens_d = cohens_d, 
                                               reward_probability = reward_probability)
            fig, axes = plt.subplots(nrows = 1, ncols = 1)
            sns.kdeplot(output["p_values"], label = "p_values", ax = axes)
            fig.suptitle("P(p-value <= {}) with {} pp, {} trials".format(significance_cutoff, npp, ntrials), fontweight = 'bold')
            axes.set_title("Power = {}% based on {} reps with ES = {}".format(np.round(power_estimate*100, 2), nreps, cohens_d))
        else: print("Criterion not found")
        axes.axvline(x = significance_cutoff, lw = 2, linestyle ="dashed", color ='k', label ='significance_cutoff')
        fig.legend(loc = 'center right')
        fig.tight_layout()
        end_time = datetime.now()
        print("\nPower analysis ended at {}; run lasted {} hours.".format(end_time, end_time-start_time))
        fig.savefig(os.path.join(plot_folder, 'Distributionplot_line{}.jpg'.format(i)))
