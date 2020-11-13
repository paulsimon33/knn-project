#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:21:38 2020

@author: paul
"""

import math

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
            matrix.append(line[:-1].split("\t"))
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

def distance(lst1, lst2) :
    """
    Euclidian distance between 2 vectors represented as lists.
    If a position is NA, this position is ingored for the calculation. 

    Parameters
    ----------
    lst1 : list
        The first vector.
    lst2 : list
        The second vector.

    Returns
    -------
    dist : float
        The euclidian distance between them.

    """
    
    if len(lst1) != len(lst2) :
        raise ValueError("Lists don't have the same length")
    
    dist = 0
    for k in range(len(lst1)) :
        if lst1[k] != "NA" and lst2[k] != "NA" :
            dist += (float(lst2[k]) -float((lst1[k]))) ** 2
    return(math.sqrt(dist))


def weights(distance_lst) :
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
        

def knn(matrix, k) :
    """
    Take a matrix with NAs and replace them with imputed data found by the
    k - Nearest Neighbours (k-NN) method.

    Parameters
    ----------
    matrix : list of lists
        Matrix with NAs.
    k : int
        Number of neighbours to consider.

    Returns
    -------
    new_matrix : list of lists
    	Matrix with NA replaced by imputed numbers.

    """
    
    new_matrix = []
    
    for row in matrix :
        # Search which positions are NAs
        NA_pos_list = [i for i in range(len(row)) if row[i] == "NA"]
        
        # If no NA, just keep the row
        if NA_pos_list == [] :
            new_matrix.append(row)
        
        # Else, find the neighbours
        else :
            neighbour_dist_list = []
            for neighbour in matrix[1:] :
                if "NA" not in neighbour :
                    neighbour_dist_list.append([neighbour, distance(row[1:], neighbour[1:])])
            neighbour_dist_list.sort(key = lambda x: x[1])
            nearest_neighbours = neighbour_dist_list[:k]
            weight_list = weights([nei[1] for nei in nearest_neighbours])
            # print("a", weight_list)
            
            # Impute the missing values
            for missing_pos in NA_pos_list :
                s = 0
                for neighbour_pos in range(k) :
                    s += weight_list[neighbour_pos] * float(nearest_neighbours[neighbour_pos][0][missing_pos])
                row[missing_pos] = s

    # return(matrix)

matrix = read_matrix("../../data/E-GEOD-10590.processed.1/test3.txt_10_modified")
modified_matrix = knn(matrix,10)
write_matrix(matrix, "../../data/E-GEOD-10590.processed.1/test3.txt_10_modified_imputed")
        
                