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


#df = pd.read_csv ('ACC1LA_70deg.csv',delimiter='comma', header=0, engine="python")
# reading all the data from the accelration file for this one trial
df = pd.read_csv ('C:/Users/Adam/Drive/Coding/GitRepos/Thesis_TAFT/Visual3d/FingerIdentification/ACC_FP Data/SA_70Deg_01 ACCFP3.csv', header=1, skiprows=[2,3,4] )

# the next step will be to integrate this data
##maybe I can just apply filtering through the Biomechanical toolkit

print (df)

Time = (df['Unnamed: 0'])
S1_ACCX = df['Sensor 1 Acc.ACCX1']
FP3Y = df['Force.Fy3']

"""
Original Code
### plotting figures next to each other
fig = plt.figure()
plt.plot(Time, Y)
plt.xlabel('Time (sec)')
plt.ylabel('EMG or FP Marks')
fig_name = 'fig2.png'
fig.set_size_inches(w=11,h=7)
fig.savefig(fig_name)

print (df['Force.Fy3'])
df['Sensor 1 Acc.ACCX1']
"""

# Total Graph! 
x = (df['Unnamed: 0'])
y1 = df['Sensor 1 Acc.ACCX1']
y2 = df['Force.Fy3']


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.plot(x, y2, 'g-', linestyle = "--")
ax1.plot(x, y1, 'r-')

ax1.set_xlabel('X data')
ax1.set_ylabel('Y1 data', color='black')
ax2.set_ylabel('Y2 data', color='black')


plt.ylim(9, 10)

plt.show ()


##### Succesful plotting. Now I will want to reduce the dataframes for the events that I would like around FP

"""
#found onset events....
#https://neurokit.readthedocs.io/en/latest/tutorials/Python.html
events = nk.find_events(df['Force.Fy3'], cut="higher")
events
"""
"""
## from neurokit 1_ uninstaled 9:00 10.24.2020
y2.plot
events = nk.find_events(df['Force.Fy3'], cut="lower")
events
"""
### 11:11pm 12.23.2020

'''
### EMG Event Detection
emg = nk.emg_simulate(duration=10, burst_number=3)
emg_cleaned = nk.emg_clean(emg)
emg_amplitude = nk.emg_amplitude(emg_cleaned)

activity, info = nk.emg_activation(emg_amplitude=emg_amplitude, method="threshold")
fig = nk.events_plot([info["EMG_Offsets"], info["EMG_Onsets"]], emg_cleaned)
fig  
'''

#detecting events from forceplate
emg_cleaned = nk.emg_clean(y2)
emg_amplitude = nk.emg_amplitude(emg_cleaned)

activity, info = nk.emg_activation(emg_amplitude=emg_amplitude, method="threshold", threshold=.5)
fig = nk.events_plot([info["EMG_Offsets"], info["EMG_Onsets"]], emg_cleaned)
fig

onset_values = info.get('EMG_Onsets')
offset_values = info.get('EMG_Offsets')
# print(onset_values)
# print (offset_values)

(onset_values [1] + offset_values [1])

a=7
b=9

d = np.dot(a, b, out=None)
