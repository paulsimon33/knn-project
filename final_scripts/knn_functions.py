#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:21:38 2020
@author: paul and mikkel

Script containing functions for performing the deletion of points in a dataset
and then applying the k-NN algorithms.
"""
import sys
import copy
import random

# Set the random seed for reproducibility
random.seed(1)


def parse_arguments(arg):
    """
    Function for parsing the argument from the command line to be used in
    the script.

    Parameters
    ----------
    arg: list
        List coming from sys.argv.

    Returns
    -------
    filename : string
        The name of the file containing the matrix.
    error_rate : int
        The percentage of missing values one wants to produce.
    k : int
        The k value for the k-NN algorithm.

    """
    
    filename = None
    error_rate = None
    k = None
    
    # Search for arguments
    for i in range(1,len(arg)):
        # Display help
        if sys.argv[i] == ('-h' or '--help'):
            print('Help')
            sys.exit(1)
        # Search for filenmae
        elif sys.argv[i] == '-f':
            filename = sys.argv[i+1]
        # Search for error rate
        elif sys.argv[i] == '-e':
            try:
                error_rate = int(sys.argv[i+1])
            except ValueError as error:
                print('Error rate must be an integer -', error)
                sys.exit(1)
        # Search for k
        elif sys.argv[i] == '-k':
            try:
                k = int(sys.argv[i+1])
            except ValueError as error:
                print('k must be an integer -', error)
                sys.exit(1)
                
    # Raise error if arguments are missing        
    if filename == None: raise Exception('Filename not provided')
    if error_rate == None: raise Exception('Error rate not provided')
    if k == None: raise Exception('k not provided')
    
    return(filename, error_rate, k)

       
def read_matrix(filename):
    """
    Read a tab separated file to create a list of lists. First row is reserved
    for headers and first column is reserved for an identifier. Only numbers
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
    
    # Open file
    try:
        infile = open(filename, 'r')
    except IOError as error:
        print("Can't open file -", error)
        sys.exit(1)

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
                try:
                    # Convert numbers to float
                    row_list[i] = float(row_list[i])
                except ValueError as error:
                    print('Invalid data - Data must be number or NA -', error)
                    sys.exit(1)
        # Add row to matrix
        matrix.append(row_list)
        line = infile.readline()
    infile.close()
    return(matrix)


def write_matrix(matrix, filename):
    """
    Write a matrix (list of lists) in the given file.
    Parameters
    ----------
    matrix : list of lists
        Matrix to write.
    file : str
        Name of the file to write in.
    Returns
    -------
    None
    """
    
    with open(filename, "w") as outfile:
        for row in matrix:
            row_list = []
            for col in row:
                row_list.append(str(col))
            print('\t'.join(row_list), file=outfile)
            
         
def produce_NAs(matrix, percentage):
    """
    Take a file and remove data from it. It creates a new file with NAs.
    
    Parameters
    ----------
    matrix : list of lists
        Matrix with all data.
    percentage : int
        From 0 to 100, pourcentage of data to erase.
    Returns
    -------
    NA_matrix : lists of lists
        Matrix with NAs.
    """
    
    # Deep copy of the matrix to keep both of them in memory
    NA_matrix = copy.deepcopy(matrix)
    
    # Calculate the total length of the dataset
    number_rows = len(matrix)-1
    number_cols = len(matrix[0])-1
    total_numbers = number_rows * number_cols
    
    # Generate numbers for positions to delete
    quantity_deleted = int(percentage/100 * total_numbers)
    positions_deleted = set(random.sample(range(total_numbers),quantity_deleted))
    
    # Replace numbers with NAs
    for row in range(1,number_rows+1):
        for col in range(1,number_cols+1):
            if (row-1) * number_cols + (col-1) in positions_deleted:
                NA_matrix[row][col] = 'NA'
    
    return(NA_matrix)


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
    
    # If the first distance is 0, then we only use 1 neighbor.
    # The first weight is 1, others are 0.
    if distance_lst[0] == 0:
        weight_lst.append(1)
        weight_lst += [0 for i in range(len(distance_lst)-1)]
        
    # Otherwise, we append weigths in the list
    else:
        for dist in distance_lst:
            denominator += 1/dist
        for dist in distance_lst:
            weight_lst.append(1/dist/denominator)
    return(weight_lst)


def knn(matrix, k):
    """
    Take a matrix with NAs and replace them with imputed data found by the
    k - Nearest Neighbors (k-NN) method.
    
    Parameters
    ----------
    matrix : list of lists
        Matrix with NAs.
    k : int
        Number of neighbors to consider.
    Returns
    -------
    new_matrix : list of lists
     	Matrix with NA replaced by imputed numbers.
    """
    
    # Create output matrix with header
    new_matrix = [matrix[0]]
    
    # Read each row in matrix
    for row_idx in range(1,len(matrix)):
        row = copy.deepcopy(matrix[row_idx])
        # Find positions of NAs and values
        NA_idx_list = [i for i in range(1,len(row)) if row[i] == 'NA']
        value_idx_list = [i for i in range(1,len(row)) if row[i] != 'NA']
        # Initialize distance dictionaries        
        row_distance_dict = dict()
        distance_dict = dict()
        
        # Calculate each missing value
        for NA_idx in NA_idx_list:
            # Update row distance dictionary with distances from last iteration
            row_distance_dict.update(distance_dict)
            # Create new distance dictionaty for this NA
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
            if k > len(distance_dict):
                raise Exception('k larger than the number of neighbors')
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
                new_value += weight_list[i] * value_list[i]
            row[NA_idx] = new_value
        
        # Add row with calculated missing values to output matrix
        new_matrix.append(row)
    
    return(new_matrix)