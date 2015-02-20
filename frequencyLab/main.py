#!/usr/bin/env python3

"""Frequency lab, lab2 for cs3130
   Author: Colby Garland
   ID#   : 5034957
   Deals with the user interaction/ main function"""

import frequency

def main():
    input_menu()

# Prints the menu, and gets the input for the file to process
def input_menu():
    print("--")
    print("Word Frequency Table Generator")
    print("Enter the name of file to process: ", end="")

    fileName = input()
   
    #process the file
    frequency.process_file(fileName)
    
main()
