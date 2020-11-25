#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:21:38 2020

@author: paul and mikkel
"""

import math
import copy
import time

def read_matrix(filename):
    """
    Read a tab separated file to create a list of lists. First row is reserved
    for headers and first columns if reserved for an identifier. Only numbers
    and NAs are accepted on the other postions.
    
    Parameters
    ----------
    file : str
        Name of the file containing the matrix.
    Returns
    -------
    matrix : list of lists
        The resulting matrix.
    """
    # matrix = []
    
    with open(filename, "r") as infile:
        # Add header to matrix
        line = infile.readline()
        matrix = [line[:-1].split("\t")]
        # Read all other lines
        line = infile.readline()
        while line != '':
            row_list = line[:-1].split("\t")
            for i in range(1,len(row_list)):
                # Raise error if value is not NA or number
                if row_list[i] != 'NA':
                    # Convert numbers to float
                    row_list[i] = float(row_list[i])
            # Add row to matrix
            matrix.append(row_list)
            line = infile.readline()
    return(matrix)
        # first_line = True
        # for line in infile:
        #     linelist = line[:-1].split("\t")
        #     if first_line == True:
        #         first_line == False
        #     else:
        #         for i in range(1,len(linelist)):
        #             if linelist[i] != 'NA':
        #                 linelist[i] = float(linelist[i])
        #         # try:
        #         #     linelist[i] = float(linelist[i])
        #         # except ValueError:
        #         #     pass
        #     matrix.append(linelist)
    return(matrix)


def write_matrix(matrix, file):
    """
    Write a matrix (list of lists) in the given file

    Parameters
    ----------
    matrix : list of lists
        Matrix to write.
    file : str
        Name of the file to write in.

    Returns
    -------
    None.

    """
    
    with open(file, "w") as outfile :
        for row in range(len(matrix)) :
            printlist = []
            for column in range(len(matrix[row])) :
                printlist.append(str(matrix[row][column]))
            print("\t".join(printlist),file = outfile)


def weights(distance_lst):
    """
    From a list of distances, return a list of weights for each position.
    This function is the implementation of (1) of (Kim et al. 2004) and is used
    for computing the weighted average.

    Parameters
    ----------
    distance_lst : list
        List of distances.

    Returns
    -------
    weight_lst : list
        List of weights to apply for calculating the average.

    """

    weight_lst = []
    denominator = 0
    for dist in distance_lst :
        denominator += 1/dist
    for dist in distance_lst :
        weight_lst.append(1/dist/denominator)
    return(weight_lst)


def knn(matrix, k):
    """
    

    Parameters
    ----------
    matrix : TYPE
        DESCRIPTION.
    k : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # Create output matrix with header
    new_matrix = [matrix[0]]
    
    # Read each row in matrix
    for row_idx in range(1,1000):
        row = copy.deepcopy(matrix[row_idx])
        # Find positions of NAs and values
        NA_idx_list = [i for i in range(1,len(row)) if row[i] == 'NA']
        value_idx_list = [i for i in range(1,len(row)) if row[i] != 'NA']
        # Create empty dictionaries for distances        
        row_distance_dict = dict()
        distance_dict = dict()
        
        # Calculate each missing value
        for NA_idx in NA_idx_list:
            # Update row distance dictionary with distances from last iteration
            row_distance_dict.update(distance_dict)
            distance_dict = dict()
            
            # Find distances to all valid rows
            for train_row_idx in range(1,len(matrix)):
                train_row = matrix[train_row_idx]
                # Continue if missing value exists in train row  
                if train_row[NA_idx] != 'NA':
                    # Initialize distance calculation                    
                    distance = 0
                    # Continue if the other values of the row exist in train row
                    for value_idx in value_idx_list:
                        if train_row[value_idx] == 'NA':
                            distance = None
                            break
                    if distance != None:
                        # Check if distance is already calculated
                        if train_row_idx in row_distance_dict:
                            distance = row_distance_dict[train_row_idx]
                        # Calculate distance between row and train row    
                        else:
                            for value_idx in value_idx_list:
                                distance += (row[value_idx] - train_row[value_idx]) ** 2
                            distance = distance ** 0.5
                        # Add index of train row and distance to dictionary    
                        distance_dict[train_row_idx] = distance
            
            # Find k nearest neighbors
            value_list = []
            distance_list = []
            for neighbor in (sorted(distance_dict, key=distance_dict.get)[0:k]):
                value_list.append(matrix[neighbor][NA_idx])
                distance_list.append(distance_dict[neighbor])
            # Calculate weights
            weight_list = weights(distance_list)

            # Calculate missing value
            new_value = 0
            for i in range(k):
                new_value += weight_list[i] * values_list[i]
            row[NA_idx] = new_value
        
        #
        new_matrix.append(row)
    
    return(new_matrix)
        
                

matrix = read_matrix("test3.txt_10_modified")

start = time.time()
new_matrix = knn(matrix, 10)
#modified_matrix = knn(matrix,12)

end = time.time()
print("Time:", end - start)

write_matrix(new_matrix, "test3_10p_10n_mikkel.txt")








# def distance(lst1, lst2) :
#     """
#     Euclidian distance between 2 vectors represented as lists.
#     If a position is NA, this position is ingored for the calculation. 

#     Parameters
#     ----------
#     lst1 : list
#         The first vector.
#     lst2 : list
#         The second vector.

#     Returns
#     -------
#     dist : float
#         The euclidian distance between them.

#     """
    
#     if len(lst1) != len(lst2) :
#         raise ValueError("Lists don't have the same length")
    
#     dist = 0
#     for k in range(len(lst1)) :
#         if lst1[k] != "NA" and lst2[k] != "NA" :
#             dist += (float(lst2[k]) -float((lst1[k]))) ** 2
#     return(math.sqrt(dist))



        

# def knn(matrix, k) :
#     """
#     Take a matrix with NAs and replace them with imputed data found by the
#     k - Nearest Neighbours (k-NN) method.

#     Parameters
#     ----------
#     matrix : list of lists
#         Matrix with NAs.
#     k : int
#         Number of neighbours to consider.

#     Returns
#     -------
#     new_matrix : list of lists
#     	Matrix with NA replaced by imputed numbers.

#     """
    
#     new_matrix = []
    
#     for row in matrix :
#         # Search which positions are NAs
#         NA_pos_list = [i for i in range(len(row)) if row[i] == "NA"]
        
#         # If no NA, just keep the row
#         if NA_pos_list == [] :
#             new_matrix.append(row)
        
#         # Else, find the neighbours
#         else :
#             new_row = copy.deepcopy(row)
#             neighbour_dist_list = []
#             for neighbour in matrix[1:] :
#                 if "NA" not in neighbour :
#                     neighbour_dist_list.append([neighbour, distance(row[1:], neighbour[1:])])
#             neighbour_dist_list.sort(key = lambda x: x[1])
#             nearest_neighbours = neighbour_dist_list[:k]
#             weight_list = weights([nei[1] for nei in nearest_neighbours])
            
#             # Impute the missing values
#             for missing_pos in NA_pos_list :
#                 s = 0
#                 for neighbour_pos in range(k) :
#                     s += weight_list[neighbour_pos] * float(nearest_neighbours[neighbour_pos][0][missing_pos])
#                 new_row[missing_pos] = s
#             new_matrix.append(new_row)

#     return(new_matrix)


        
                