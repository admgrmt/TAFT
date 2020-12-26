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


def previous_val (value):
    fin_acc = 1
    init_acc = 0
    velocity = 0
    while fin_acc <= value:
        velocity = ((((df.loc[fin_acc]['Acceleration'] + df.loc[init_acc]['Acceleration'])/2)*1) + velocity)
        fin_acc = fin_acc + 1
        init_acc = init_acc + 1
        print(velocity)
    return velocity
    
print(previous_val(11))
