"""
Demo of basic reading and plotting of Polysomnogrophy files with mne
"""
import mne
import matplotlib.pyplot as plt
import os


def read_eeg(edf_fp):
    data = mne.io.read_raw_edf(edf_fp)
    print("This EDF file has the following channels: ")
    channels = read_channels(data)
    for channel in channels:
        print(channel)
    del data
    print("\nFor this example, we will limit our analysis to any available EEG channels.")
    eeg_ch = {'EEG F3-M2', 'EEG F4-M1', 'EEG C3-M2', 'EEG C4-M1', 'EEG O1-M2', 'EEG O2-M1', 'EEG CZ-O1'}
    exclude_ch = list(set(channels) - eeg_ch)
    data = mne.io.read_raw_edf(edf_fp, exclude=exclude_ch)
    channels = read_channels(data)
    print("The new channels are the following:")
    for channel in channels:
        print(channel)
    return data


def plot_data(data_signal, channels, beg, end):
    fig, axs = plt.subplots(len(channels))
    for i in range(len(channels)):
        axs[i].plot(data_signal[i][beg:end])
        axs[i].set_title(channels[i])
    plt.show()


def read_channels(data):
    return list(data.ch_names)


def read_annotations(data):
    all_annotations = []
    for item in data.annotations:
        all_annotations.append(item['description'])
    return all_annotations


def main():
    edf_fp = 'filepath.EDF' # put your filepath here
    data = read_eeg(edf_fp)
    print("You can read the annotations from an EDF+ file.")
    all_anns = read_annotations(data)
    print("The 100th annotation in the file is {}".format(all_anns[100]))
    print("You can extract the raw signal data for your own analysis.")
    raw_data = data.get_data()
    print("Here is a simple plot of a small section of the EEG data.")
    plot_data(raw_data, data.ch_names, 10000, 10500)


if __name__ == '__main__':
    main()
