#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:21:38 2020

@author: paul
"""

import math

def distance(lst1, lst2) :
    """
    Euclidian distance between 2 vectors represented as lists

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
        dist += (lst2[k] - lst1[k]) ** 2
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
    k - Nearest Neighbours (k-NN) method

    Parameters
    ----------
    matrix : list of lists
        Matrix with NAs.
    k : int
        Number of neighbours to consider.

    Returns
    -------
    None.

    """
    
    for row in matrix :
        # Search which positions are NAs
        NA_pos_list = [i for i in row if row[i] == "NA"]
        
        # Compute distance with row if rows have the information at the wished
        # positions 