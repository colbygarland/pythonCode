#!/usr/bin/env python3

"""Frequency lab, lab2 for cs3130
   Author: Colby Garland
   ID#   : 5034957
   Deals with the file handling/processing functions"""

dictionary = {}
LETTER_COUNT = 23 # Max word size
MAXNUMHISTO = 10 # Max number of stars the histogram will print out


# Opens the appropriate file and processes the file
def process_file(fileName):

    letterCounter = 0 # Counter to keep track of how long current word is
 
    try:
        lines = open(fileName, "r")
    
        for line in lines:
            inWord = False # Flag to determine if in the middle of a word to add
            word = ""
            letterCounter = 0
            for ch in line:
                if ch.isalpha() and letterCounter <= LETTER_COUNT:
                    inWord = True
                    word += ch
                    letterCounter += 1
                else:
                    if inWord:
                        if word not in dictionary:
                            dictionary[word] = 1
                            inWord = False
                            word = ""
                            letterCounter = 0
                        else:
                            dictionary[word] += 1
                            inWord = False
                            word = ""
                            letterCounter = 0
            

        lines.close()
        dump_dictionary()
    except FileNotFoundError as err:
        print("The file specified is not in the directory")

# Dumps the dictionary in a nicely formatted way, also shows a histogram of the dictionary
def dump_dictionary():
    

    print("--")
    print("File Processing Complete.")
    print("\nWord Frequency Table")
    print("WORD                 FREQUENCY")
    print("------------------------------")

    for key in dictionary:
        print("{0:<25}".format(key) + format(dictionary[key], "2"))

    print("\nHistogram")
    print("WORD                 FREQUENCY")
    print("------------------------------")
    
    for key in dictionary:
        print("{0:<25}|".format(key, dictionary[key]), end="")

        if dictionary[key] < 10:
            print("X" * dictionary[key])
        else:
            rest = dictionary[key] - MAXNUMHISTO
            print("X" * 10 + "(" + str(rest) + ")")
