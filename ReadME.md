[![Uni](https://img.shields.io/badge/University-Ghent%20University-brightgreen)](https://img.shields.io/badge/University-Ghent%20University-brightgreen)
[![AY](https://img.shields.io/badge/Academic%20Year-2021--2022-yellow)](https://img.shields.io/badge/Academic%20Year-2021--2022-yellow)

# COmputational Power Analysis using Simulations "COMPASS" toolbox 

This toolbox has been developed to estimate the power of obtaining adequate learning rate estimates <img width="28" alt="image" src="https://user-images.githubusercontent.com/73498415/151129769-337c084f-005b-4e56-8b27-6506eac7c684.png"> when using a basic Rescorla-Wagner model (basic RW-model) to mimic participants’ behaviour on a probabilistic reversal learning task. 

## The model and task currently implemented in COMPASS   
### Probabilistic reversal learning task 
In this task participants try to maximise the reward they get by implicitly learning the stimulus-response mapping rules. 
There are two stimuli (coded as 0 and 1) and two possible responses (coded as 0 and 1) in this design. 
Two rules are used throughout the experiment: the first rule is ‘respond with response 0 to stimulus 1 and with a response 1 to stimulus 0’; the second rule reverses this stimulus-response mapping. 
Rule reversals can happen. Feedback is given on each trial (0 = no reward, 1 = reward), but this feedback is only in a certain defined percentage of the trials congruent with the current rule. 

### The basic RW-model
The basic Rescorla-Wagner model (RW-model) is used to mimic participants’ behaviour in this task. 
The core of the model is formed by the delta-learning rule and the softmax choice rule. 
The model has two free parameters: the learning rate (LR) and the inverse temperature 
<img width="17" alt="image" src="https://user-images.githubusercontent.com/73498415/151129877-e1cb8115-b6b9-41b0-bc8e-35f331c0b027.png">

## Important limitation: the required computational time
The computational time for these power estimates is quite large. This computational time depends on several factors: the number of trials, the number of participants and the number of repetitions included in the power estimate. Therefore, the option is included to run the power analysis on multiple cores. This happens when the user defines the 'full_speed' option as 1; if this option is activated, all minus two cores on the computer  doing the power analysis will be used.  
When using the template for the Input_file.csv on GitHub, the power analysis takes ca. 10 minutes when running on a single core and ca. 2 minutes when running on a computer with 16 cores. It is important to realise that any increase in the number of trials, participants or repetitions used for the power analysis will increase the computation time. 
COMPASS gives an estimate of how long it will take to calculate the power for each line within this Input_file, at the beginning of the execution of each line. This estimate is based on the time it takes to execute a single repetition and calculated by multiplying the total number of repetitions included by the time required for a single repetition, divided by the number of cores that are used in the power analysis. If you want to stop the process whilst running, you can use 'ctrl + C' in the anaconda prompt shell. This will completely stop the execution of the script. 

## Power estimation with COMPASS
The power to obtain adequate parameter estimates is calculated by repeatedly conducting parameter recovery analyses. 
This process is repeated in order to estimate the probability or power of a successful parameter recovery analysis. 

  ```power = number of successful parameter recovery analyses / total number of parameter recovery analyses```

Each parameter recovery analysis consists of the following four steps: 
  1. Sample npp participants from the population ( npp parameter sets)
  2. Simulate data for each participant (= each parameter set)
  3. Estimate the best fitting parameters for each participant given the simulated data. These are the ‘recovered parameters’. 
  4. Evaluate whether the parameter recovery analysis was successful. This depends on the parameter recovery criterion defined by the researcher. 	
     - _correlation_: <img width="113" alt="image" src="https://user-images.githubusercontent.com/73498415/151130378-6b8ca89b-2cab-4705-8b76-25cb10836898.png">
     - _group_difference_: <img width="103" alt="image" src="https://user-images.githubusercontent.com/73498415/151130416-00e39026-47ee-4edd-a2b9-806047f493cb.png"> (success when <img width="106" alt="image" src="https://user-images.githubusercontent.com/73498415/151130479-162c7e01-6304-4938-af11-6991226d283e.png">)

## How to use the PCM toolbox 
1. Download all files from this github-folder and store them in the same folder on your computer. https://github.com/CogComNeuroSci/internship-maud/tree/main/PowerAnalysis/Version1.0

2. Open Input_file.csv and adapt the variables to match your design and your parameter recovery requirements.
   <img width="634" alt="image" src="https://user-images.githubusercontent.com/73498415/151140185-b217a37f-8e7e-4618-baa7-89c205b28c49.png">
   * _ntrials_: <img width="77" alt="image" src="https://user-images.githubusercontent.com/73498415/151137007-c8318365-0942-4d57-be2d-480ce4b7a8ce.png">
     **number of trials within the experiment (minimal 5)**
   * _nreversals_: <img width="92" alt="image" src="https://user-images.githubusercontent.com/73498415/151136975-2d8958a1-6ebd-4d96-b265-e6fd15cb968b.png">
     **number of rule reversals within the eximerpent**
   * _npp_: <img width="77" alt="image" src="https://user-images.githubusercontent.com/73498415/151136935-8c53fabc-8781-4d87-85ad-3e80be36b9ad.png">
     **number of participants within the experiment (minimal 5)**
     - when criterion = _correlation_: _npp_ = total number of participants
     - when criterion = _group_difference_: _npp_ = number of participants per group
   * _reward_probability_: <img width="76" alt="image" src="https://user-images.githubusercontent.com/73498415/151136895-ee404362-53c4-4a63-b731-7e2b0fb0ce2b.png">
     **The probability that reward will be congruent with the current stimulus-response mapping rule.**
     - If reward_probability = 0.80, the feedback will be congruent with the rule in 80% of the trials.
   * _full_speed_: <img width="71" alt="image" src="https://user-images.githubusercontent.com/73498415/151136836-6f18c18e-5550-43d6-a7c7-f6698efd344a.png">
     **Define whether you want to do the power analysis at full speed.**
     - 0 = only one core will be used (slow)
     - 1 = (all-2) cores will be used (much faster, recommended unless you need your computer for other intensive tasks such as meetings)
   * _criterion_: <img width="146" alt="image" src="https://user-images.githubusercontent.com/73498415/151136776-0c719157-bcdf-45f9-bed7-4f7ac3fd5c1c.png">
     **The criterion that will be used to evaluate the success of the parameter recovery analysis.**
     - correlation: <img width="123" alt="image" src="https://user-images.githubusercontent.com/73498415/151135353-6f4bd7bc-3883-4d9c-8a9c-29f7c72d1f38.png">
     - group_difference: Statistic = p_value associated with T-Value obtained by a two-sample t-test comparing 
        <img width="46" alt="image" src="https://user-images.githubusercontent.com/73498415/151135539-18e7567c-15f4-40b6-80aa-4634e91ca900.png">
       and <img width="44" alt="image" src="https://user-images.githubusercontent.com/73498415/151135576-20b3faed-59a8-4976-be53-3d5f7edc2143.png">
   * _cut_off_: <img width="58" alt="image" src="https://user-images.githubusercontent.com/73498415/151136720-b971148b-6b15-45cd-8669-89a205548302.png">
     **The cut-off against which the statistic of interest will be compared to evaluate the success of each parameter recovery analysis**
     - success with correlation criterion when <img width="118" alt="image" src="https://user-images.githubusercontent.com/73498415/151136512-43c58e48-3057-4b34-8bde-41b8fcac2822.png"> - recommended cut_off: 0.75
     - success with group difference criterion when <img width="106" alt="image" src="https://user-images.githubusercontent.com/73498415/151136561-30851df0-8e2b-4f64-b442-65c4855677be.png"> - recommended cut_off: 0.05
   * _nreps_: <img width="78" alt="image" src="https://user-images.githubusercontent.com/73498415/151136671-ace0ae88-b1cc-4021-b6bf-d80bf016d567.png">
     **Number of parampeter recovery analyses that will be conducted to estimate the power**
     - Recommended number: 1000
   * _output_folder_: <img width="26" alt="image" src="https://user-images.githubusercontent.com/73498415/151136622-4e008d74-9f97-4e0d-a863-3db947e818b2.png">
     **Path to the folder where the output-figure(s) will be stored**
     - e.g. "C:\Users\maudb\Downloads"
    
    This file can contain multiple rows with different requirements or design-options. 
    If the file contains multiple rows, the power will be estimated using the variables defined within each row sequentially. 
    This allows the researcher to elegantly compare the effect of changing a certain variable on the power estimate. 
    <img width="634" alt="image" src="https://user-images.githubusercontent.com/73498415/151140016-1f564b1d-8532-42b2-96da-b3d6a5e5ff63.png">

3. Run the PowerAnalysis.py script using the correct Anaconda 3 environment. 
   
   To recreate the programming environment (**in Windows**), simply download our power_estimation environment file https://github.com/CogComNeuroSci/internship-maud/blob/main/PowerAnalysis/Version1.0/environment.yml and take the following steps:
   * Install Anaconda 3 by following their [installation guide](https://docs.anaconda.com/anaconda/install/windows/)
   * When the installation is complete, open an Anaconda prompt
   * Go to the directory where ```power_estimation.yml``` is located using ```cd```
   * Now, run: ```conda env create --file power_estimation.yml```
   * Allow the installation of all required packages
   
   To execute the power analysis take the following steps: 
   * Open Anaconda prompt
   * Now, run: ```conda activate power_estimation```
   * Go to the directory where ```Functions.py```, ```PowerAnalysis.py``` and ```Input_file.csv``` are located using ```cd```
   * Now, run: ```python PowerAnalysis.py```

4. Check the output in the shell & the stored figure(s) in the _output_folder_
   * _power estimate_: the probability to obtain adequate parameter estimates
   * _mean failed LR estimates_: the mean % of participants whose learning rate estimate was implausible;
     an LR estimate is considered implausible when <= 0.1
   * _probability density plot of the Statistic of interest_: a plot visualising the obtained values for the Statistic of interest in all power recovery analyses
     - x-axis: values for the statistic of interest (correlation or p-value)
     - y-axis: probability density for each value

    Example output: 
    
    <img width="577" alt="image" src="https://user-images.githubusercontent.com/73498415/151138147-b33804d4-071a-42df-8cd6-2672523bce81.png">
    
    <img width="466" alt="image" src="https://user-images.githubusercontent.com/73498415/151139153-1d17653d-86a4-4ec7-8c7c-00821b9d2cf9.png">

# Contact

- Internship student: Maud Beeckmans 
    * [E-mail me at Maud (dot) Beeckmans (at) UGent (dot) be](mailto:Maud.Beeckmans@UGent.be)
- Supervising PhD researcher: Pieter Verbeke
    * [E-mail me at pjverbek (dot) Verbeke (at) UGent (dot) be](mailto:pjverbek.Verbeke@UGent.be)
- Supervising PhD researcher: Pieter Huycke
    * [E-mail me at Pieter (dot) Huycke (at) UGent (dot) be](mailto:Pieter.Huycke@UGent.be)
- Supervising professor: Tom Verguts
    * [E-mail me at Tom (dot) Verguts (at) UGent (dot) be](mailto:Tom.Verguts@UGent.be)

**Last edit: 26 January 2022**
