# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 21:02:46 2020

@author: Adam
"""

from pyomeca import Analogs
import pyomeca as pym
import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats

data_path = "C:/Users/Adam/Drive/Adam_G_Thesis/4_Data/Pilot/CalibrationSettingsVicon/12_09_2020_TurningFinger/C3d/LA_70deg.c3d"

channels = ["ACCX1", "ACCY1", "ACCZ1"]
analogs = Analogs.from_c3d(data_path, usecols=channels, prefix_delimiter=".")


# forces = [
#     "Force.Fx3",
#     "Force.Fy3",
#     "Force.Fz3",
#     ]



emg=analogs
# fp3 = Analogs.from_c3d(data_path, suffix_delimiter=".", usecols=forces)

emgshort=emg.sel(channel="channels", time=10)

emg.plot(x="time", col="channel", col_wrap=2);
# column is clearly the variables we are graphing/graphs, X is the time,
# and col_wrap specifies how many per width on plot

emg_processed = (
    emg.meca.band_pass(order=2, cutoff=[10, 425])
    .meca.center()
    .meca.abs()
    .meca.low_pass(order=4, cutoff=5, freq=emg.rate)
    .meca.normalize()
)

emg_processed.plot(x="time", col="channel", col_wrap=3);

emg_processed.name = "EMG"
emg_processed.attrs["units"] = "%"
emg_processed.time.attrs["units"] = "seconds"

emg_processed.plot(x="time", col="channel", col_wrap=3);

fig, axes = plt.subplots(ncols=2, figsize=(10, 4))

emg_processed.mean("channel").plot(ax=axes[0])
axes[0].set_title("Mean EMG activation")

emg_processed.plot.hist(ax=axes[1], bins=50)
axes[1].set_title("EMG activation distribution");

emg_dataframe = emg_processed.meca.to_wide_dataframe()
emg_dataframe.plot.box(showfliers=False);



## got some graphs. Now I need to correlate them with the force plate events
## having some sort of bound on either side - maybe like 100 frames to recognize the events from the force plats
## I am not sure currently how to recognize the actions on either side of the events...