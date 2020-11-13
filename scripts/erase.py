#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 17:20:47 2020

@author: paul
"""

import random
random.seed(0)


def produce_NAs(file, percentage) :
    """
    Take a file and remove data from it. It creates a new file with NAs.
    
    Parameters
    ----------
    file : str
        Input file with all data.
    percentage : int
        From 0 to 100, pourcenatge of data to erase.

    Returns
    -------
    None.

    """
    
    try :
        with open(file, "r") as infile :
            with open(file + "_" + str(percentage) + "_modified", "w") as outfile :
                
                lines = infile.readlines()
                
                number_lines = len(lines)-1
                number_columns = len(lines[1][:-1].split("\t"))-1
                # The -1 are to be sure we do ot consider the first row and first col
                
                print(number_lines)
                print(number_columns)
                
                # Generate numbers for positions to delete
                total_numbers = number_lines*number_columns
                quantity_deleted = int(percentage/100*total_numbers)
                positions_deleted = set(random.sample(range(total_numbers),quantity_deleted))
                
                print(positions_deleted)
                
                # Now delete them
                n_line = -1 # To copy the first line, the 2nd will be line 0
                
                for line in lines :
                    tmp_list = line[:-1].split("\t")
                    new_line = [tmp_list[0]]
                    for k in range(number_columns) :
                        if n_line*number_columns+k in positions_deleted :
                            new_line.append("NA")
                        else :
                            new_line.append(tmp_list[k+1])
                    print("\t".join(new_line), file = outfile)
                    n_line += 1
                    
                
    except IOError as error :
        print("Can't open file", error)

produce_NAs("../../data/E-GEOD-10590.processed.1/test3.txt", 10)
                
                




















