"""
Demonstrates getting epoch data object from mne based on sleep stage annotations
"""
import matplotlib.pyplot as plt
import mne

from read_edf import read_annotations


def get_stage_epochs(mne_data, sleep_stage='all'):
    """ Get the mne epochs object for all annotated sleep stages

    Assumes an epoch length of 30 seconds
    """
    if sleep_stage == 'all':
        event_id = get_available_stages(read_annotations(mne_data))
    else:
        event_id = get_one_stage(sleep_stage)

    if len(event_id) > 0:
        events, _ = mne.events_from_annotations(mne_data, event_id=event_id, chunk_duration=30.)
        tmax = 30. - 1. / mne_data.info['sfreq']
        epochs_data = mne.Epochs(raw=mne_data, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)
        return epochs_data
    else:
        return None


def get_one_stage(sleep_stage):
    """Return an event dictionary for one sleep stage

    input options are "all", 1, 2, 3, 4
    """
    event_id = dict()
    if sleep_stage == 1:
        event_id['Sleep stage N1'] = 1
    elif sleep_stage == 2:
        event_id['Sleep stage N2'] = 2
    elif sleep_stage == 3:
        event_id['Sleep stage N3'] = 3
    elif sleep_stage == 4:
        event_id['Sleep stage R'] = 4
    else:
        print("Error, please enter \"all\", 1, 2, 3, or 4 for sleep stage")
    return event_id


def get_available_stages(all_annotations):
    """Return n event dictionary mapping sleep stages to integers

    Not all EDF files will have all sleep stages present, so this function
    checks to see which sleep stages are in the annotations.

    Assumes sleep stages are annotated 'Sleep stage N1' etc.
    """
    event_id = dict()
    if 'Sleep stage N1' in all_annotations:
        event_id['Sleep stage N1'] = 1
    if 'Sleep stage N2' in all_annotations:
        event_id['Sleep stage N2'] = 2
    if 'Sleep stage N3' in all_annotations:
        event_id['Sleep stage N3'] = 3
    if 'Sleep stage R' in all_annotations:
        event_id['Sleep stage R'] = 4
    return event_id


def get_raw_epochs(epochs):
    raw_data = []
    for item in epochs[:2]:
        raw_data.append(item)
    return raw_data[0]


def main():
    edf_fp = 'Filename.EDF'
    data = mne.io.read_raw_edf(edf_fp)
    epochs = get_stage_epochs(data, 1)
    raw_epochs = get_raw_epochs(epochs)
    print("displaying the fifth epoch in sleep stage 1")
    plt.plot(raw_epochs[5])
    plt.show()


if __name__ == '__main__':
    main()
