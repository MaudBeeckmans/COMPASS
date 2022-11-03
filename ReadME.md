[![Uni](https://img.shields.io/badge/University-Ghent%20University-brightgreen)](https://img.shields.io/badge/University-Ghent%20University-brightgreen)
[![AY](https://img.shields.io/badge/Academic%20Year-2021--2022-yellow)](https://img.shields.io/badge/Academic%20Year-2021--2022-yellow)

# COmputational Power Analysis using Simulations "COMPASS" toolbox 

This toolbox has been developed to estimate the power of obtaining adequate learning rate estimates <img width="15" alt="image" src="https://user-images.githubusercontent.com/73498415/156181828-ee3782a8-c534-4458-82df-0c7b7323f4c9.png"> when using a Rescorla-Wagner model (RW model) to mimic participants’ behaviour on a probabilistic reversal learning task. 

## The model and task currently implemented in COMPASS   
### Probabilistic reversal learning task 
In this task participants try to maximise the reward they get by implicitly learning the stimulus-response mapping rules. 
There are two stimuli (coded as 0 and 1) and two possible responses (coded as 0 and 1) in this design. 
Two rules are used throughout the experiment: the first rule is ‘respond with response 0 to stimulus 1 and with a response 1 to stimulus 0’; the second rule reverses this stimulus-response mapping. 
Rule reversals can happen. Feedback is given on each trial (0 = no reward, 1 = reward), but this feedback is only in a certain defined percentage of the trials congruent with the current rule. 

### The RW model
The RW model is used to mimic participants’ behaviour in this task. 
The core of the model is formed by the delta-learning rule and the softmax choice rule. 
The model has two free parameters: the learning rate 𝛼 and the inverse temperature 𝜆.

## Important limitation: the required computational time
The computational time for these power estimates is quite large. This computational time depends on several factors: the number of trials, the number of participants and the number of repetitions included in the power estimate. Therefore, the option is included to run the power analysis on multiple cores. This happens when the user defines the 'full_speed' option as 1; if this option is activated, all minus two cores on the computer  doing the power analysis will be used.  
When using the template for the InputFile_IC.csv and the InputFile_GD.csv on GitHub, the power analysis takes ca. 10 minutes when running on a single core and ca. 2 minutes when running on a computer with 16 cores. It is important to realise that any increase in the number of trials, participants or repetitions used for the power analysis will increase the computation time. 
COMPASS gives an estimate of how long it will take to calculate the power for each line within this Input_file, at the beginning of the execution of each line. This estimate is based on the time it takes to execute a single repetition and calculated by multiplying the total number of repetitions included by the time required for a single repetition, divided by the number of cores that are used in the power analysis. If you want to stop the process whilst running, you can use 'ctrl + C' in the anaconda prompt shell. This will completely stop the execution of the script. 

## Power estimation with COMPASS
The power to obtain adequate parameter estimates is calculated by repeatedly conducting parameter recovery analyses. 
This process is repeated in order to estimate the probability or power of a successful parameter recovery analysis. 

  ```power = number of successful parameter recovery analyses / total number of parameter recovery analyses```

Each parameter recovery analysis consists of the following four steps: 
  1. Sample npp participants from the population (npp parameter sets)
  2. Simulate data for each participant (= each parameter set)
  3. Estimate the best fitting parameters for each participant given the simulated data. These are the ‘recovered parameters’. 
  4. Evaluate whether the parameter recovery analysis was successful. This depends on the parameter recovery criterion defined by the researcher. 	
     - _internal_correlation_: <img width="100" alt="image" src="https://user-images.githubusercontent.com/73498415/156185769-cad73153-2b53-4707-a266-67c376a00c79.png">
     - _group_difference_: <img width="50" alt="image" src="https://user-images.githubusercontent.com/73498415/156185831-2f654264-82a4-44e9-abd3-676033fb6cd9.png"> (success when p_value ≼ cut_off)
## How to use COMPASS.
1. Download all files from this github-folder and store them in the same folder on your computer.

2. Adapt the relevant input file depending on whether you want to rely on the internal correlation criterion (IC) or the group difference criterion (GD). 
	- internal correlation: <img width="80" alt="image" src="https://user-images.githubusercontent.com/73498415/156186624-bf2d4c13-4da9-47bb-a9a6-34c27ddeebbc.png">
	- group difference: <img width="300" alt="image" src="https://user-images.githubusercontent.com/73498415/156186716-bf9b9ab2-86bc-4045-9af7-61b0e9996536.png">

2a) IC: Open the InputFile_IC.csv and adapt the variables to define your model, statistic parameters and cut-off (tau). 
<img width="634" alt="image" src="https://user-images.githubusercontent.com/73498415/151140185-b217a37f-8e7e-4618-baa7-89c205b28c49.png">
* _ntrials_: integer 𝜖 [5, +∞[
	**number of trials within the experiment (minimal 5)**
* _nreversals_: integer 𝜖 [0, ntrials[
	**number of rule reversals within the eximerpent**
* _npp_: integer 𝜖 [5, +∞[ 
	**total number of participants within the experiment (minimal 5)**
* _meanLR_: float 𝜖 [0, 1]
	**mean of the assumed population distribution of learning rates**
* _sdLR_: float 𝜖 [0, 1]
	**sd of the assumed population distribution of learning rates**
* _meanInverseTemperature_: float 𝜖 [0, 1]
	**mean of the assumed population distribution of inverse temperatures**
* _sdInverseTemperature_: float 𝜖 [0, 1]
	**sd of the assumed population distribution of inverse temperatures**
* _reward_probability_: float 𝜖 [0, 1] 
	**The probability that reward will be congruent with the current stimulus-response mapping rule.**
	- If reward_probability = 0.80, the feedback will be congruent with the rule in 80% of the trials.
* _tau_: float 𝜖 [0, 1] 
	**the value against which the obtained statistic will be compared to define significance of the repetition.**
	- correlation: cut_off = minimally desired correlation - recommended: 0.75
* _full_speed_: integer (0 or 1)
	**Define whether you want to do the power analysis at full speed.**
	- 0 = only one core will be used (slow)
	- 1 = (all-2) cores will be used (much faster, recommended unless you need your computer for other intensive tasks such as meetings)
* _nreps_: integer 𝜖 [1, +∞[ 
	**Number of repetitions that will be conducted to estimate the power**
	- Recommended number: minimal 100
* _output_folder_: string
	**Path to the folder where the output-figure(s) will be stored**
	- e.g. "C:\Users\maudb\Downloads"

2b) GD: Open the InputFile_GD.csv and adapt the variables to define your model, statistic parameters and typeIerror. 
* _ntrials_: integer 𝜖 [5, +∞[
	**number of trials within the experiment (minimal 5)**
* _nreversals_: integer 𝜖 [0, ntrials[
	**number of rule reversals within the eximerpent**
* _npp_group_: integer 𝜖 [5, +∞[ 
	**number of participants within the experiment (minimal 5)**
* _meanLR_g1_: float 𝜖 [0, 1]
	**mean of the assumed population distribution of learning rates for group 1**
* _sdLR_: float 𝜖 [0, 1]
	**sd of the assumed population distribution of learning rates for group 1** 
* _meanLR_g2_: float 𝜖 [0, 1]
	**mean of the assumed population distribution of learning rates for group 2**
* _sdLR_g2_: float 𝜖 [0, 1]
	**sd of the assumed population distribution of learning rates for group 2** 
* _meanInverseTemperature_g1_: float 𝜖 [0, 1]
	**mean of the assumed population distribution of inverse temperatures for group 1**
* _sdInverseTemperature_g1_: float 𝜖 [0, 1]
	**sd of the assumed population distribution of inverse temperatures for group 1**
* _meanInverseTemperature_g2_: float 𝜖 [0, 1]
	**mean of the assumed population distribution of inverse temperatures for group 2**
* _sdInverseTemperature_g2_: float 𝜖 [0, 1]
	**sd of the assumed population distribution of inverse temperatures for group 2**
* _reward_probability_: float 𝜖 [0, 1] 
	**The probability that reward will be congruent with the current stimulus-response mapping rule.**
	- If reward_probability = 0.80, the feedback will be congruent with the rule in 80% of the trials.
* _TypeIerror_: float 𝜖 [0, 1] 
	**The allowed probability to make a type I error; the significance level**
	- standard (and recommended) value: 0.05
* _full_speed_: integer (0 or 1)
	**Define whether you want to do the power analysis at full speed.**
	- 0 = only one core will be used (slow)
	- 1 = (all-2) cores will be used (much faster, recommended unless you need your computer for other intensive tasks such as meetings)
* _nreps_: integer 𝜖 [1, +∞[ 
	**Number of repetitions that will be conducted to estimate the power**
	- Recommended number: minimal 100
* _output_folder_: string
	**Path to the folder where the output-figure(s) will be stored**
	- e.g. "C:\Users\maudb\Downloads"
    
Both Input files can contain multiple rows with different requirements or design-options. 
If the file contains multiple rows, the power will be estimated using the variables defined within each row sequentially. 
This allows the researcher to elegantly compare the effect of changing a certain variable on the power estimate.     
<img width="634" alt="image" src="https://user-images.githubusercontent.com/73498415/151140016-1f564b1d-8532-42b2-96da-b3d6a5e5ff63.png">

3. Run the PowerAnalysis.py script using the correct Anaconda 3 environment. 
   
   To recreate the programming environment (**in Windows**), simply download our environment file (environment.yml) and take the following steps:
   * Install Anaconda 3 by following their [installation guide](https://docs.anaconda.com/anaconda/install/windows/)
   * When the installation is complete, open an Anaconda prompt
   * Go to the directory where ```environment.yml``` is located using ```cd```
   * Now, run: ```conda env create --file environment.yml```
   * Allow the installation of all required packages
   
   To execute the power analysis take the following steps: 
   * Open Anaconda prompt
   * Now, run: ```conda activate pyPower```
   * Go to the directory where ```Functions.py```, ```PowerAnalysis.py``` and ```Input_file.csv``` are located using ```cd```
   * Now, run: ```python PowerAnalysis.py IC``` or ```python PowerAnalysis.py GD``` depending on whether you want to use the internal correlation criterion or the group difference criterion

4. Check the output in the shell & the stored figure(s) in the _output_folder_
   * _power estimate_: the probability to obtain adequate parameter estimates
   * _mean failed 𝛼 estimates_: the mean % of participants whose learning rate estimate was implausible;
     an 𝛼 estimate is considered implausible when ≼ 0.1
   * _probability density plot of the Statistic of interest_: a plot visualising the obtained values for the Statistic of interest in all power recovery analyses
     - x-axis: values for the statistic of interest (correlation or p-value)
     - y-axis: probability density for each value

    Example output: 
    
    <img width="800" alt="image" src="https://user-images.githubusercontent.com/73498415/157639967-e9a5643e-9796-416d-a1c4-df43b89f3dc7.png">
    <img width="500" alt="image" src="https://user-images.githubusercontent.com/73498415/157640378-76d551ef-4524-4d15-8a4b-2174756bd9eb.png">
    
# Contact

- Internship student: Maud Beeckmans 
    * [E-mail me at Maud (dot) Beeckmans (at) UGent (dot) be](mailto:Maud.Beeckmans@UGent.be)
- Supervising PhD researcher: Pieter Verbeke
    * [E-mail me at pjverbek (dot) Verbeke (at) UGent (dot) be](mailto:pjverbek.Verbeke@UGent.be)
- Supervising PhD researcher: Pieter Huycke
    * [E-mail me at Pieter (dot) Huycke (at) UGent (dot) be](mailto:Pieter.Huycke@UGent.be)
- Supervising professor: Tom Verguts
    * [E-mail me at Tom (dot) Verguts (at) UGent (dot) be](mailto:Tom.Verguts@UGent.be)

**Last edit: 10 March 2022**
