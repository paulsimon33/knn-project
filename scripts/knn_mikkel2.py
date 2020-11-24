#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:30:08 2020

@author: merik
"""

import time
import math

# NA_idx = []
# number_idx = []

# for i in range(1,len(matrix)):
#     NA_idx.append([])
#     number_idx.append([])
#     for j in range(1,len(matrix)):
#         if matrix[i][j] == 'NA':
#             NA_idx[i].append(j)
#         else:
#             number_idx[i].append(j)
            
# for i in range(1,len(NA_idx)):
#     for j in range(1,len(NA_idx[i])):
#         for k in range(1,len(matrix)):
#             if i != k:
#                 for l in range(1,len(matrix[k])):
                    




# for test_row in range(1,len(matrix)):
#     for test_col in range(1,len(matrix[test_row])):
#         if matrix[test_row][test_col] == 'NA':
#             for train_row in range(1,len(matrix)):
#                 if test_row != train_row:
#                     for train_col in range(1,len(matrix[train_row])):
#                         if 

def read_matrix(file) :
    """
    Read a tab separated file to create a list of lists.
    Parameters
    ----------
    file : str
        Name of the file containing the matrix.
    Returns
    -------
    matrix : list of lists
        The resulting matrix.
    """
    matrix = []
    
    with open(file,"r") as infile :
        for line in infile :
            linelist = line[:-1].split("\t")
            for i in range(1,len(linelist)):
                try:
                    linelist[i] = float(linelist[i])
                except ValueError:
                    pass
            matrix.append(linelist)
    return(matrix)

matrix = read_matrix('test3.txt_10_modified')


         

start_time = time.time()

def knn_mikkel(matrix, k) :
    for row_idx in range(1,1000):
        
        # print(row_idx)
        
        row = matrix[row_idx]
        NA_idx_list = [i for i in range(1,len(row)) if row[i] == 'NA']
        number_idx_list = [i for i in range(1,len(row)) if row[i] != 'NA']
        
        last_distance_dict = dict()
        distance_dict = dict()
        
        for NA_idx in NA_idx_list:
            
            last_distance_dict.update(distance_dict)
            distance_dict = dict()
              
            for train_row_idx in range(1,len(matrix)):
                train_row = matrix[train_row_idx]
                
                # print('T', train_row_idx)
                
                if train_row[NA_idx] != 'NA':
                    
                    no_NA_flag = True
                    for number_idx in number_idx_list:
                        if train_row[number_idx] == 'NA':
                            no_NA_flag = False
                            break
                        
                    if no_NA_flag == True:
                        
                        if train_row_idx in last_distance_dict:
                            distance = last_distance_dict[train_row_idx]
                            
                        else:
                            distance = 0
                            for number_idx in number_idx_list:
                                distance += (row[number_idx] - train_row[number_idx]) ** 2
                            distance = distance ** 0.5
                            
                        distance_dict[train_row_idx] = distance
            
            dist_list = []
            values_list = []
            for neighbor in sorted(distance_dict, key=distance_dict.get, reverse = True)[0:k] :
                values_list += matrix[neighbor][NA_idx]
                dist_list += distance_dict[neighbor]
            weight_list = weigths(dist_list)
            
            new_value = 0
            for i in range(k) :
                new_value += weight_list[i] * values_list[i]

            
                    
                    

                    
end_time = time.time()
print(end_time - start_time)

