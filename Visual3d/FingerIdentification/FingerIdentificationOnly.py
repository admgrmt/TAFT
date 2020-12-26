# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:06:30 2020

@author: Adam
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 16:25:29 2020
*Modified 7:52PM

@author: Adam
"""

import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame



#df = pd.read_csv ('ACC1LA_70deg.csv',delimiter='comma', header=0, engine="python")
# reading all the data from the accelration file for this one trial
#df = pd.read_csv ('C:/Users/Adam/Drive/Coding/GitRepos/Thesis_TAFT/Visual3d/FingerIdentification/ACC_FP Data/SA_70Deg_01 ACCFP3.csv', header=1, skiprows=[2,3,4] )

# the next step will be to integrate this data
##maybe I can just apply filtering through the Biomechanical toolkit

df2 = df.iloc[0:29077, 1:25]

Sensor = "Sensor 6 Acc.ACCY6"

#=============================================================
#### inserting formula with integration 
#### attempting to make new column of data for integration of each signal

#inserts a blank data frame for the integrated values
df2.insert(24, Sensor + " Constant", 0)
df2.insert(25, Sensor + " Velocity", 0)
df2.insert(26,  Sensor + " Position", 0)

# df2[Sensor + " Constant"] = df2[Sensor].subtract(df2.iloc[0][Sensor])
df2[Sensor + " Constant"] = df2[Sensor].subtract(0)

# creates a function to integrate a column of values on a 1 m/s change  
# this particular function was to integrate acceleration into "average velocity" on 1 m/s interval    
def avg_integrate_velocity (value):
    fin_value = 1
    init_value= 0
    change_output = 0
    while fin_value <= value:
        change_output = ((((df2.loc[fin_value][Sensor + " Constant"] + df2.loc[init_value][Sensor + ' Constant'])/2)*1) + change_output)
        df2.loc[fin_value, Sensor + ' Velocity'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output

avg_integrate_velocity(29076) 

# df2["Sensor 1 Acc.ACCX1 Velocity"] = df2["Sensor 1 Acc.ACCX1 Velocity"].subtract(df2.iloc[0]['Sensor 1 Acc.ACCX1 Velocity'])


###=====================================
### going to try and integrate velocity data to positional data
###=====================================

# manipulating earlier function to apply velocity values for the change - making new function
def avg_integrate_position (value):
    fin_value = 1
    init_value= 0
    change_output = 0.00000001
    while fin_value <= value:
        change_output = ((((df2.loc[fin_value][Sensor + ' Velocity'] + df2.loc[init_value][Sensor + ' Velocity'])/2)*1) + change_output)
        df2.loc[fin_value, Sensor + ' Position'] = change_output
        fin_value = fin_value + 1
        init_value = init_value + 1
        #print(change_output)
    return change_output

avg_integrate_position(29076)

# df2["Sensor 1 Acc.ACCX1 Position"] = df2["Sensor 1 Acc.ACCX1 Position"].subtract(df2.iloc[0]['Sensor 1 Acc.ACCX1 Position'])

#===================================================

#detecting events from forceplate and plott
emg_cleaned = nk.emg_clean(y2)
emg_amplitude = nk.emg_amplitude(emg_cleaned)
activity, info = nk.emg_activation(emg_amplitude=emg_amplitude, method="threshold", threshold=.5)

# fig = nk.events_plot([info["EMG_Offsets"], info["EMG_Onsets"]], emg_cleaned)
# fig


onset_values = info.get('EMG_Onsets')
offset_values = info.get('EMG_Offsets')
print(onset_values)
print (offset_values)


your_list = onset_values
Onset_Values = DataFrame(your_list,columns=['Onset Values'])
your_list = onset_values
Offset_Values = DataFrame(your_list,columns=['Offset Values'])

Onset_Values_Range = Onset_Values - 300 
Offset_Values_Range = Offset_Values + 300 


### ===========================
### Test graph for acceleration function
### ===========================

# GraphDFTime = Time.iloc[Temo1:Temo2]
# GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
# GraphDFFP3 = FP3.iloc[Temo1:Temo2]

Time = df['Unnamed: 0']
ACC = df2[Sensor + ' Constant']
FP3 = df['Force.Fy3']

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACC.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel(Sensor + ' Acceleration', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()


### ==========================
### Test graph for velocity
### ==========================


Time = df['Unnamed: 0']
ACC = df2[Sensor + ' Velocity']
FP3 = df['Force.Fy3']

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACC.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel(Sensor + ' Velocity', color='black')
ax2.set_ylabel('FP3 Y Axis', color='black')


plt.show ()

### ===========================
### Test graph for position function
### ===========================
### should plot full graphs to view patterns first
### I.e. not using 'temo' but using loc 1:29077

Time = df['Unnamed: 0']
ACC = df2[Sensor + ' Position']
FP3 = df['Force.Fy3']

Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
Temo2 = Offset_Values_Range.iloc[0]['Offset Values']

GraphDFTime = Time.iloc[Temo1:Temo2]
GraphDFACCX1 = ACC.iloc[Temo1:Temo2]
GraphDFFP3 = FP3.iloc[Temo1:Temo2]


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')

ax1.set_xlabel('Time')
ax1.set_ylabel(Sensor + ' Position', color='black')
ax2.set_ylabel('FP3', color='black')


plt.show ()
