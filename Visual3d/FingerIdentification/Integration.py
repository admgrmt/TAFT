# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:13:11 2020

@author: Adam
"""

import pandas as pd


"""
def summation(value):
    i = 1
    sum_value = 0
    while i <= value:
        sum_value = sum_value + i
        i = i + 1
    print(sum_value)
    return sum_value

print(summation(11))

"""

df = pd.read_csv ('C:/Users/Adam/Desktop/Example.csv', header=0)

#inserts a blank data frame for the integrated values
df.insert(3, "Velocity Integration", "N/A")

# creates a function to integrate a column of values on a 1 m/s change  
# this particular function was to integrate acceleration into "average velocity" on 1 m/s interval    
def avg_integrate_values (value):
    fin_value = 1
    init_value= 0
    change_output = 0
    while fin_value <= value:
        change_output = ((((df.loc[fin_value]['Acceleration'] + df.loc[init_value]['Acceleration'])/2)*1) + change_output)
        df.loc[fin_value,'Velocity Integration'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output
    
#print(avg_integrate_values(11))
