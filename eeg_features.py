"""
Demonstrate some simple feature extraction from EEG data
"""
import numpy as np
import matplotlib.pyplot as plt
import mne
import os

import read_edf
from eeg_epochs import get_stage_epochs


def get_power_spectrum(epochs):
    """EEG power spectral density

    Use Welch's method to get the power spectral density for frequencies from 1-30

    fmin: minimum frequency of interest
    fmax: maximum frequency of interest
    Checking frequencies 1-30 here
    returns shape (num epochs, num channels, num frequencies)
    """
    psds, freqs = mne.time_frequency.psd_welch(epochs, picks='eeg', fmin=0.5, fmax=30.)
    # Normalize the PSDs - try 0 mean normalization?
    psds /= np.sum(psds, axis=-1, keepdims=True)
    return psds, freqs


def avg_power_band(psds, freqs):
    """Average power over specific frequency bands

    Take the average power over a specific frequency interval.
    Will return 5 values per channel for num epochs
    Shape is (num epochs, 5* num channels)

    Adapted from this tutorial:
    https://11743-1301584-gh.circle-artifacts.com/0/dev/auto_tutorials/plot_sleep.html
    """
    # specific frequency bands
    freq_bands = {"delta": [0.5, 4.5],
                  "theta": [4.5, 8.5],
                  "alpha": [8.5, 11.5],
                  "sigma": [11.5, 15.5],
                  "beta": [15.5, 30]}
    X = []
    for fmin, fmax in freq_bands.values():
        psds_band = psds[:, :, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
        X.append(psds_band.reshape(len(psds), -1))
    return np.concatenate(X, axis=1)


def main():
    edf_fp = 'Filename.EDF'
    data = read_edf.read_eeg(edf_fp)
    epochs_data = get_stage_epochs(data, sleep_stage=3)
    psds, freqs = get_power_spectrum(epochs_data)
    print("plotting the power spectral density for the first epoch of sleep stage 3")
    psd = psds[0][0]
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.plot(psd)
    plt.show()


if __name__ == '__main__':
    main()
