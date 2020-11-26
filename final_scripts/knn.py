#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:17:22 2020

@author: paul and mikkel

Main script, used to call all the functions definied in knn_functions.py
"""

import time
from knn_functions import *

# Record start time       
start_time = time.time()

# Read arguments
filename, error_rate, k = parse_arguments(sys.argv)

# Load matrix from file
matrix = read_matrix(filename)

# Replace values with NAs
NA_matrix = produce_NAs(matrix, error_rate)

# Calculate values of NAs
knn_matrix = knn(NA_matrix, k)

# Print kNN matrix to output file
write_matrix(knn_matrix, filename + '_k' + str(k) + '_e' + str(error_rate) + '.txt')

# Record end time
end_time = time.time()
elapsed_time = (end_time - start_time) / 60

# Display complete message
print('kNN matrix created for', filename)
print('k =', k, ' --  Error rate =', str(error_rate) + '%', ' --  Runtime =', '{:.2f}'.format(elapsed_time), 'min')
print('File saved as ' + filename + '_k' + str(k) + '_e' + str(error_rate) + '.txt')
