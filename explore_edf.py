"""
Some explanations and helpful information about the NCH Polysomnogrophy EDF+ files
"""
import matplotlib.pyplot as plt
import mne
import re


def annotations_info(edf_filepath):
    """
    Compare annotation times to times based on the number of points in the signal.
    """
    data = mne.io.read_raw_edf(edf_filepath)
    freq = data.info['sfreq']
    raw_data = data.get_data()
    num_data_points = raw_data.shape[1]
    print("There are {} data points in each channel".format(num_data_points))
    secs_data = num_data_points/256.0
    hrs_data = secs_data/(60.0*60.0)
    print("The total study length in seconds is {}, or {} hrs".format(secs_data, hrs_data))
    print("The annotations can be retrieved by calling data.annotations. "
          "The recording starts at 0.0 seconds, though the first annotation may have a later onset."
          "\'Lights Off\' indicates the beginning of the study")
    lights_off, lights_on = lights_time(data.annotations)
    print("Lights Off occurs at {} seconds".format(lights_off))
    print("Lights On occurs at {} seconds".format(lights_on))
    print("There are {} annotations".format(len(data.annotations)))
    print("After Lights On, annotations will probably say \'Sleep stage ?\' "
          "and will default to 30 second duration")
    print("Because of this, mne will truncate the last annotation duration to "
          "match the study length based on the number of data samples")
    print("This is the cause of the RuntimeWarning: Limited 1 annotation(s) that were expanding outside the data range")
    print("The last recorded annotation occurs at {} with a duration "
          "of {}".format(data.annotations[-1]['onset'], data.annotations[-1]['duration']))
    print("Therefore we can see that the total is {}, therefore matching our study length {}, "
          "calculated from the number of data points".format(data.annotations[-1]['onset'] + data.annotations[-1]['duration'], secs_data))
    print("Finally, the function _read_annotations_edf below is pulled "
          "from mne with some modifications to simplify it. If you have any concerns about the annotations "
          "pulled by mne, you can use this function to read the annotations "
          "directly from an EDF+ file for troubleshooting purposes.")


def data_info(edf_filepath):
    data = mne.io.read_raw_edf(edf_filepath)
    freq = data.info['sfreq']
    print("The sampling frequency is {} hz ({} samples per second)".format(freq, freq))
    raw_data = data.get_data()
    print("The EDF file has {} channels: {}".format(len(data.ch_names), data.ch_names))
    print("The Patient Event channel (if present) is not the annotation channel, and will usually just consist of 0.0")
    num_data_points = raw_data.shape[1]
    print("There are {} data points in each channel".format(num_data_points))
    print("checking the data for any flat signals")
    bad_channels = find_flat_signals(raw_data)
    print("These channels have flat signals: ")
    for i in bad_channels:
        print(data.ch_names[i])
    lights_off, lights_on = lights_time(data.annotations)
    # I'm going to assume just one lights off and lights on
    lon_index = int(lights_off[0]*256.0)
    loff_index = int(lights_on[0]*256.0)
    print("\n\nLights Off occurs at {} seconds, which is data point {}".format(lights_off, lon_index))
    print("Lights On occurs at {} seconds, which is data point {}".format(lights_on, loff_index))
    # Just plotting a random channel
    print("Compare full plot with lights off/on")
    plt.subplot(1, 2, 1)
    plt.plot(raw_data[6])
    plt.subplot(1, 2, 2)
    plt.plot(raw_data[6][lon_index:loff_index])
    plt.show()


def find_flat_signals(raw_data):
    """
    Check to see which channels have 2 or fewer unique values
    """
    duds = []
    for i, channel in enumerate(raw_data):
        if len(set(channel)) < 3:
            duds.append(i)
    return duds


def lights_time(data_annotations):
    lights_off = []
    lights_on = []
    for item in data_annotations:
        if item['description'] == 'Lights Off':
            lights_off.append(item['onset'])
        elif item['description'] == 'Lights On':
            lights_on.append(item['onset'])
    return lights_off, lights_on


def _read_annotations_edf(edf_filepath):
    """Annotation File Reader.
    Parameters
    ----------
    edf_filepath : ndarray (n_chans, n_samples) | str
        Path to EDF+ file with annotation channel.
    Returns
    -------
    onset : array of float, shape (n_annotations,)
        The starting time of annotations in seconds after ``orig_time``.
    duration : array of float, shape (n_annotations,)
        Durations of the annotations in seconds.
    description : array of str, shape (n_annotations,)
        Array of strings containing description for each annotation. If a
        string, all the annotations are given the same description. To reject
        epochs, use description starting with keyword 'bad'. See example above.
    """
    # This detects Time Stamped Annotations Lists (TALs) which is the format
    # used to store the annotations in EDF+
    pat = '([+-]\\d+\\.?\\d*)(\x15(\\d+\\.?\\d*))?(\x14.*?)\x14\x00'

    with open(edf_filepath, encoding='latin-1') as annot_file:
        triggers = re.findall(pat, annot_file.read())

    events = []
    for ev in triggers:
        onset = float(ev[0])
        duration = float(ev[2]) if ev[2] else 0
        for description in ev[3].split('\x14')[1:]:
            if description:
                events.append([onset, duration, description])

    return zip(*events) if events else (list(), list(), list())


def main():
    # Replace with your directory path and filename
    samp_edf = 'Filename.EDF'
    annotations_info(samp_edf)
    data_info(samp_edf)


if __name__ == '__main__':
    main()
