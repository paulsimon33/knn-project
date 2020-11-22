#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:34:49 2020

@author: paul
"""

import math
import matplotlib.pyplot as plt

def rms_error(complete_file, imputed_file, per_missing) :
    """
    Compute the RMS error of the file with imputed values.

    Parameters
    ----------
    complete_file : str
        Name of the file with the starting dataset.
    imputed_file : str
        Name of the file umputed with k-NN.
    per_missing : int
        Percentage of missing values.

    Returns
    -------
    rms : float
        The RMS error.

    """
    
    rms = 0.
    number_lines = 0
    
    ref_file = open(complete_file, "r")
    imp_file = open(imputed_file, "r")
    
    # Jump the headers
    ref_line = ref_file.readline()
    ref_line = ref_file.readline()
    imp_line = imp_file.readline()
    imp_line = imp_file.readline()
    
    number_columns = len(ref_line.split()[1:])
    
    while ref_line != "" and imp_line != "" :
        number_lines += 1
        ref_list = ref_line.split()[1:]
        imp_list = imp_line.split()[1:]
        
        for i in range(len(ref_list)) :
            if float(ref_list[i]) != float(imp_list[i]) :
                rms += (float(ref_list[i]) - float(imp_list[i])) ** 2
        
        ref_line = ref_file.readline()
        imp_line = imp_file.readline()
    
    ref_file.close()
    imp_file.close()
    
    total_numbers = number_lines*number_columns
    num_missing = int(per_missing/100*total_numbers)
    
    return(math.sqrt(rms/num_missing))
        
        
complete_file = "../../data/E-GEOD-10590.processed.1/test3.txt"
imputed_file = "../../data/E-GEOD-10590.processed.1/test3_10_modified_imputed.txt"
print(rms_error(complete_file, imputed_file, 10))
