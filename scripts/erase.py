#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 17:20:47 2020

@author: paul
"""


def produce_NAs(file, percentage) :
    """
    Take a file and removes data from it. It creates a new file with NAs.
    
    Parameters
    ----------
    file : str
        Input file with all data.
    percentage : int
        From 0 to 100, pourcenatge of data to erase

    Returns
    -------
    None.

    """
    
    try :
        with open(file, "r") as infile :
            with open(file + "_" + str(percentage) + "_modified", "w")\
            as outfile :
                number_lines = len(infile.readlines())
                # First line kept in the new file
                line = infile.readline()
                number_columns = len(line.split("\t"))
                outfile.write(line)
                print(number_lines)
                print(number_columns)
                
                # PROBLEM : We cannot do .realines() and .readline() with the
                # same file
                
                
    except IOError as error :
        print("Can't open file", error)

produce_NAs("../../data/E-GEOD-10590.raw.1/GSM266997.txt", 10)
                
                




















