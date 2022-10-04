# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 14:21:39 2022

@author: maudb
"""

import numpy as np


"""Probleem functies: LR kan niet groter dan één zijn."""

def LR_transformation(LR = 0.8): 
    x = np.log(LR/(1-LR))
    return x
    
def LR_retransformation(transformed_LR = 1.3):
    original_LR = np.exp(transformed_LR)/(1+np.exp(transformed_LR))
    return original_LR

LR = 0.01

trans_LR = LR_transformation(LR)
print(trans_LR)
orig_LR = LR_retransformation(trans_LR)
print(orig_LR)

#%%
def InverseT_transformation(InverseT = 1): 
    x = np.log(InverseT)
    return x

def InverseT_retransformation(transformed_InverseT = 3):
    original_InverseT = np.exp(transformed_InverseT)
    return original_InverseT

invT = 5

trans_invT = InverseT_transformation(invT)
print(trans_invT)
orig_invT = InverseT_retransformation(trans_invT)
print(orig_invT)




#%%Check for distributions in the "default"
dist = np.random.normal(loc = 0.7, scale = 0.2, size = 200)
print("min: {}, max: {}".format(np.min(dist), np.max(dist)))