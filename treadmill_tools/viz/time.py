"""
General visualization functions
"""
import numpy as np
import matplotlib.pyplot as plt
from spikeinterface import *
 

def plot_traces(recording: BaseRecording, chans: list, time: tuple,
                figsize=(15, 25)):
    
    times = recording.get_times()
    frames = np.argwhere((time[0] <= times) & (times <= time [1]))

    array = recording.get_traces(
        start_frame=frames[0],
        end_frame=frames[-1],
        channel_ids=chans
    )

    fig, axes = plt.subplots(
        array.shape[1],
        figsize=figsize,
        sharex='all',
        sharey='none'
    )
    for ax, trace, chan in zip(axes, array.T, chans):
        ax.plot(times[frames[:-1]], trace)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_ylabel(chan[-4:], rotation=0)
        ax.set_yticks([])

    axes[-1].set_xlim([time[0], time[1]])
    axes[-1].set_label(['Time (s)'])

    print(len(times[frames[:-1]]))

    return