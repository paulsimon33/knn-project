#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:34:49 2020

@author: paul and mikkel


Script for analysing the result obtained with our implementation of k-NN.
It draws plots RMS = f(k) and time = f(k) for several values of percentages of
missing data.
NOTE : This full script runs in approximately 2 hours and 40 minutes.
"""

import math
import matplotlib.pyplot as plt
from knn_functions import *
import time

def rms_error(reference_matrix, imputed_matrix, per_missing) :
    """
    Compute the RMS error between the imputed matrix and the reference matrix.
    
    Parameters
    ----------
    reference_matrix : list of lists
        Matrix with complete dataset.
    imputed_matrix : list of lists
        Matrix with imputed data.
    per_missing : int
        Percenatge of points deleted and then imputed.

    Returns
    -------
    rms : float
        The RMS error.

    """
    
    # Initialisation of RMS as a float
    rms = 0.
    
    # Error handling if the dimensions of both matrices don't match
    if len(reference_matrix) != len(imputed_matrix) :
        raise ValueError("Not the same number of row in each matrix")
    else :
        for i in range(1,len(reference_matrix)) :
            if len(reference_matrix[i]) != len(imputed_matrix[i]) :
                raise ValueError("Not the same number of columns")
            
            # Calculation of the RMS
            else :
                 for j in range(1, len(reference_matrix[i])) :
                     if reference_matrix[i][j] != imputed_matrix[i][j] :
                         rms += (reference_matrix[i][j] - imputed_matrix[i][j]) ** 2
    
    # Calculation of the number of missing value
    total_numbers = len(reference_matrix) * len(reference_matrix[0])
    num_missing = int(per_missing/100*total_numbers)
    
    return(math.sqrt(rms/num_missing))

    
# Initializing k values and percenatges values
k_list = [i for i in range(1,11)] + [i for i in range(12,21,2)] + \
    [i for i in range(25,41,5)]  
percentages = [5, 10, 15, 20, 25, 50]
 
# And the matrix that will contain [k, per_missing, rms, time]
rms_time_matrix = []

# Choosing a reference matrix
matrix_ref = read_matrix("../final_data/test_10000.txt")

# For each percentage, simulate missing points
for per in percentages :
    matrix_na = produce_NAs(matrix_ref, per)
    
    # For each k and missing value, impute values by knn
    for k in k_list :
        start = time.time()
        new_matrix = knn(matrix_na, k)
        rms = rms_error(matrix_ref, new_matrix, per)
        t = time.time() - start
        
        rms_time_matrix.append([k,per,rms,t])

# Save the matrix in a file if any error occurs
with open("rms_time_matrix.txt", "w") as infile :
    for elt in rms_time_matrix :
        print(*elt, file = infile)

# Read it back for further analysis
# rms_time_matrix = []
# with open("rms_time_matrix.txt", "r") as infile :
#     for line in infile :
#         rms_time_matrix.append(line.split())
# rms_time_matrix = rms_time_matrix[:]



# Now plot using matplolib.pyplot

# First, plot the RMS against k for different values of missing percentages.
plt.figure()
for j in range(5):
    rms_list = []
    for i in range(len(k_list)) :
        rms_list.append(float(rms_time_matrix[len(k_list)*j+i][2]))    
    plt.plot(k_list, rms_list, 'o', label = "% missing ="+ str(rms_time_matrix[len(k_list)*j][1]))

# The value of 50% is managed differently because it produces an error
# for k = 20.
rms_list = []
for i in range(13) :
    rms_list.append(float(rms_time_matrix[5*len(k_list)+i][2]))
plt.plot(k_list[:13], rms_list, 'o', label = "% missing ="+ str(rms_time_matrix[len(k_list)*5][1]))

# Some plotting parameters and save it as a PNG file
plt.xlabel("k")
plt.ylabel("RMS")
plt.legend()
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('RMS_against_k.png', dpi=100)


# Second plot, time for computation against k for different missing percentages.
# The process is the same but with the time instead of the RMS.
plt.figure()
time_list = []
for j in range(5):
    time_list = []
    for i in range(len(k_list)) :
        time_list.append(float(rms_time_matrix[len(k_list)*j+i][3]))    
    plt.plot(k_list, time_list, 'o', label = "% missing ="+ str(rms_time_matrix[len(k_list)*j][1]))

time_list = []
for i in range(13) :
    time_list.append(float(rms_time_matrix[5*len(k_list)+i][3]))
plt.plot(k_list[:13], time_list, 'o', label = "% missing ="+ str(rms_time_matrix[len(k_list)*5][1]))

plt.xlabel("k")
plt.ylabel("time (s)")
plt.legend()
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('time_against_k.png', dpi=100)
