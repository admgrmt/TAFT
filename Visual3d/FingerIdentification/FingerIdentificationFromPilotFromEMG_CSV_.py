# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:06:30 2020
@author: Adam
Last Modified: 03:14PM 20200108
"""

###=====================================
#Loading Libraries
###=====================================

import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

##==========================================================
## Automating the process
## This for loop should grab all an acceleration signals for all three of the conditions
## For this pilot EXPLICITLY (could be exanded for other conditions)
##==========================================================

C3x1_5="G:/My Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.12.30.TAFTPilot/CSV/3x1.5_5_x_30_sec_Rep_3.20.csv"
C3x3="G:/My Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.12.30.TAFTPilot/CSV/3x3_SecondTrial_5_x_30_sec_Rep_4.9.csv"
C180="G:/My Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.12.30.TAFTPilot/CSV/180_5_x_30_sec_Rep_3.26.csv"
C6x3="G:/My Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.12.30.TAFTPilot/CSV/6x3_5_x_30_sec_Rep_3.14.csv"
##=============================================================
## Setting up the for loop
##=============================================================

filename=[C3x1_5, C3x3, C180, C6x3]
for name in filename:
    
    condition = name.lstrip("G:/My Drive/Adam_G_Thesis/4_Data/Pilot/Raw_data/Raw_EMG_Data/2020.12.30.TAFTPilo")
    
    ###================================================================
    #df = pd.read_csv ('ACC1LA_70deg.csv',delimiter='comma', header=0, engine="python")
    # because this file is importing as CSV from the direct emgworks files (portable collection)
    ## we will change the data frame parameters
    ## FP3 will act as one of the footswitches...
    ###================================================================
    
    df = pd.read_csv (name, delimiter=',')
    
    
    ## ALL acc SIGNALS + FS A (R & L) 
    ## Only works from EMG Works
    
    df2 = df.iloc[:,[2,3,5,7,11,13,15,19,21,23,27,29,31,33,35]]
    df2 = df2.iloc[0:4444]
    count_row = len(df2.index)  # gives number of row count
    count_col = df2.shape[1]  # gives number of col count
    
    footswitch = df2['Trigno FSR Adapter 15: FSR 15.B']
    
    
    
    
    #Footswitch values are included in the back indexes that I DO NOT want to calculate
    
    ###================================================================
    # the next step will be to integrate this data
    # generatiing a new dataframe that excludes force data
    ###================================================================
    
    
    ###================================================================
    #picking a sensor to integrate and graph from the data
    # this currrent senso: "R BICEPS FEMORIS: Acc 12.Y" is RBF 
    ###================================================================
    
    # X[s.1]
    # L HEEL: Acc 1.X
    # L HEEL: Acc 1.Y
    # L HEEL: Acc 1.Z
    # L TOE: Acc 2.X
    # L TOE: Acc 2.Y
    # L TOE: Acc 2.Z
    # L SOLEUS: Acc 3.X
    # L SOLEUS: Acc 3.Y
    # L SOLEUS: Acc 3.Z
    # COM C7: Acc 4.X
    # COM C7: Acc 4.Y
    # COM C7: Acc 4.Z
    # Trigno FSR Adapter 15: FSR 15.A
    # Trigno FSR Adapter 15: FSR 15.B

    
    # format "R VASTUS MEDIALIS: Acc 6.Y"
    Sensor = "COM C7: Acc 4.X"
    Time = 'X[s].1'
    
    df2.plot(x = Time, y = Sensor , kind = 'scatter', s=2.00)
    plt.show()	
    
    print("this is the mean")
    sensor_mean= df2[Sensor].mean()
    print(sensor_mean)
    
    # Adding blank frames to add integrated files
    
    df2[Sensor + ' Constant']=0
    df2[Sensor + ' Velocity']=0
    df2[Sensor + ' Position']=0
    
    
    
    ###================================================================
    # inserting formula with integration 
    # attempting to make new column of data for integration of each signal
    #inserts a blank data frame for the integrated values of acc=constant, velocity, and position
    ###================================================================
    
    
    # df2[Sensor + " Constant"] = df2[Sensor].subtract(df2.iloc[0][Sensor])
    df2[Sensor + " Constant"] = df2[Sensor].subtract(sensor_mean)
    #at the moment, constant is same as OG signal
    
    
    ###================================================================
    # creates a function to integrate a column of values on a 1 m/s change  
    # this particular function was to integrate acceleration into "average velocity" on 1 m/s interval    
    ###================================================================
    
    def avg_integrate_velocity (value):
        fin_value = 1
        init_value= 0
        change_output = 0
        while fin_value <= value:
            change_output = ((((df2.loc[fin_value][Sensor + " Constant"] + df2.loc[init_value][Sensor + ' Constant'])/2)/1) + 0)
            df2.loc[fin_value, Sensor + ' Velocity'] = change_output
            fin_value = fin_value + 1
            init_value = init_value + 1
            #print(change_output)
        return change_output
    
    avg_integrate_velocity(count_row-1) 
    
    
    ###=====================================
    ### going to try and integrate velocity data to positional data
    ###=====================================
    
    # manipulating earlier function to apply velocity values for the change - making new function
    def avg_integrate_position (value):
        fin_value = 1
        init_value= 0
        change_output = 0
        while fin_value <= value:
            change_output = ((((df2.loc[fin_value][Sensor + ' Velocity'] + df2.loc[init_value][Sensor + ' Velocity'])/2)/1) + 0)
            df2.loc[fin_value, Sensor + ' Position'] = change_output
            fin_value = fin_value + 1
            init_value = init_value + 1
            #print(change_output)
        return change_output
    
    avg_integrate_position(count_row-1)
    
    ###=====================================
    #detecting events from forceplate and plott
    ###=====================================
    
    # RFS was sensor 15
    y2 = footswitch.iloc[0:(count_row)]
    emg_cleaned = nk.emg_clean(y2)
    emg_amplitude = nk.emg_amplitude(emg_cleaned)
    activity, info = nk.emg_activation(emg_amplitude=emg_amplitude, method="threshold", threshold=.7)
    
    #fig = nk.events_plot([info["EMG_Offsets"], info["EMG_Onsets"]], emg_cleaned)
    # fig
    
    
    onset_values = info.get('EMG_Onsets')
    offset_values = info.get('EMG_Offsets')
    print(onset_values)
    print (offset_values)
    
    
    your_list = onset_values
    Onset_Values = DataFrame(your_list,columns=['Onset Values'])
    your_list = onset_values
    Offset_Values = DataFrame(your_list,columns=['Offset Values'])
    
    Onset_Values_Range = Onset_Values - 100 
    Offset_Values_Range = Offset_Values + 100 
    
    
    ### ===========================
    ### Test graph for acceleration function
    ### ===========================
    
    Time = df2['X[s].1']
    ACC = df2[Sensor + ' Constant']
    FP3 = y2
    
    
    ### If we would like to hone in on a Force Peak ||| grab appropriate index or peak# from onset/offset
    ### Replace Graph Values wiith .iloc of Temo1:Temo2 set for index
    ### Replace for Constant, Velocity, Position
    
    # Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
    # Temo2 = Offset_Values_Range.iloc[0]['Offset Values']
    
    # i.e. 
    
    # GraphDFTime = Time.iloc[Temo1:Temo2]
    # GraphDFACCX1 = ACCX1.iloc[Temo1:Temo2]
    # GraphDFFP3 = FP3.iloc[Temo1:Temo2]
    
    
    GraphDFTime = Time.iloc[1:count_row]
    GraphDFACCX1 = ACC.iloc[1:count_row]
    GraphDFFP3 = FP3.iloc[1:count_row]
    
    plt.figure(dpi=1200)
    fig, ax1 = plt.subplots()
    ax1.title.set_text("Acceleration || " + condition)
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
    
    
    Time = df2['X[s].1']
    ACC = df2[Sensor + ' Velocity']
    FP3 = y2
    
    #Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
    #Temo2 = Offset_Values_Range.iloc[0]['Offset Values']
    
    GraphDFTime = Time.iloc[1:count_row]
    GraphDFACCX1 = ACC.iloc[1:count_row]
    GraphDFFP3 = FP3.iloc[1:count_row]
    
    plt.figure(dpi=1200)
    fig, ax1 = plt.subplots()
    ax1.title.set_text("Velocity || " + condition)
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
    
    Time = df2['X[s].1']
    ACC = df2[Sensor + ' Position']
    FP3 = y2
    
    #Temo1 = Onset_Values_Range.iloc[0]['Onset Values']
    #Temo2 = Offset_Values_Range.iloc[0]['Offset Values']
    
    GraphDFTime = Time.iloc[1:count_row]
    GraphDFACCX1 = ACC.iloc[1:count_row]
    GraphDFFP3 = FP3.iloc[1:count_row]
    
    plt.figure(dpi=1200)
    fig, ax1 = plt.subplots()
    ax1.title.set_text("Position || "+ condition)
    ax2 = ax1.twinx()
    ax2.plot(GraphDFTime, GraphDFFP3, 'g-', linestyle = "--")
    ax1.plot(GraphDFTime, GraphDFACCX1, 'r-')
    
    ax1.set_xlabel('Time')
    ax1.set_ylabel(Sensor + ' Position', color='black')
    ax2.set_ylabel('FP3', color='black')
    
    
    plt.show ()

#===============
# Going to try and graph a X vs Y graph
#===============

#need to take the Pos(x) value from this sensor data COM X, and plot it vs the sensor Y


