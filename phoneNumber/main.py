#!/usr/bin/env python3

""" Phone number lab assignment #2 for 
    cs3130
    Author: Colby Garland
    ID#   : 5034957 """

import re

def main():
    menu()
    

""" Prints the menu and accepts input """
def menu():
    print("----------------------------")
    print("-- Phone Number Generator --")
    print("-- Press <enter> to Quit  --")
    print("----------------------------")

    while True:
        print("Enter a 10 digit phone number: ", end="")
        num = input()
        if num == '':
            break
        else:
            # regex to parse phone number based on -, , and )
            rx1 = r'(\d{3})[- )]*(\d{3})[- )]*(\d{4})'

            if len(num) < 10:
                print("Sorry phone number needs exactly 10 digits")
            else:
                # search using the regex above
                phoneNum = re.search(rx1, num)
                try:
                    # put the numbers into appropriate categories for display
                    areaCode, first3, last4 = phoneNum.groups()
                    print("Number is " + "(" + areaCode + ")" + " " + first3 + " " + last4)
                except AttributeError as err:
                    print("Characters other than digits, hypens, space and parantheses detected")
                

main()
    
