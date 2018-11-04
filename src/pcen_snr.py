import scipy.signal
import numpy as np
import scipy 
import matplotlib.pyplot as plt
import librosa
import librosa.display


def detect_activity(y, sr,
        n_mels=128, fmin=1000, fmax=11025, 
        hop_length=512, gain=0.8, bias=10, power=0.25, pcen_time_constant=0.06, eps=1e-06,
        medfilt_time_constant=None, normalized=True,
        peak_threshold=0.45, activity_threshold=0.2):
    """
    This function detects the segments of sound activity in a waveform and returns the start and
    end time of each sound event. 
    
    Parameters
    ----------
    y : np.ndarray 
        The input signal

    sr : number > 0 [scalar]
        The audio sampling rate
        
    n_mels : int > 0 [scalar]
        number of Mel bands to generate

    fmin : float >= 0 [scalar]
        lowest frequency (in Hz)

    fmax : float >= 0 [scalar]
        highest frequency (in Hz). If None, use fmax = sr / 2.0

    hop_length : int > 0 [scalar]
        The hop length of `S`, expressed in samples

    gain : number >= 0 [scalar]
        The gain factor.  Typical values should be slightly less than 1.

    bias : number >= 0 [scalar]
        The bias point of the nonlinear compression (default: 2)

    power : number > 0 [scalar]
        The compression exponent.  Typical values should be between 0 and 1.
        Smaller values of `power` result in stronger compression.

    pcen_time_constant : number > 0 [scalar]
        The time constant for IIR filtering, measured in seconds.

    eps : number > 0 [scalar]
        A small constant used to ensure numerical stability of the filter.

    median_time_constant : float >= 0 
        The time constant for Median filtering, measured in seconds.
        
    normalized : boolean
        Whether to normalize the pcen_snr output to between 0 and 1.
        
    peak_threshold : float >= 0
        The threshold for peak-picking function.
        
    activity_threshold : float >= 0
        The threshold for defining the start and end timestamps of segments.
        
    Returns
    -------
    start_times : np.ndarray, nonnegative 
        The start times of voice activities detected in signal y (seconds).
        
    end_times : np.ndarray, nonnegative 
        The end times of voice activities detected in signal y (seconds).
        
    """
    # 1. Compute mel-frequency spectrogram
    melspec = librosa.feature.melspectrogram(
        y, sr=sr, fmin=fmin, fmax=fmax, n_mels=n_mels)
    logmelspec = librosa.power_to_db(melspec)
    
    # 2. Compute per-channel energy normalization (PCEN-SNR)
    pcen = librosa.core.pcen(melspec, sr=sr, gain=gain, bias=bias,
        power=power, time_constant=pcen_time_constant, eps=eps)
    
    # 3. compute PCEN-SNR detection function
    pcen_snr = np.max(pcen,axis=0) - np.min(pcen,axis=0)
    pcen_snr = librosa.power_to_db(pcen_snr / np.median(pcen_snr))
    if normalized:
        pcen_snr = pcen_snr / np.max(pcen_snr)
        
    # 4. Apply median filtering.
    if medfilt_time_constant is not None:
        kernel_size = 1 + 2 * round(medfilt_time_constant * sr - 0.5)
        pcen_snr = scipy.signal.medfilt(pcen_snr, kernel_size=kernel_size)
    
    # 5. Extract active segments.
    activity, start, end = threshold_activity(
        pcen_snr, peak_threshold, activity_threshold)
    
    # 6. Convert indices to seconds.
    start_times = np.round(np.array(start) * hop_length / sr, 3)
    end_times = np.round(np.array(end) * hop_length / sr, 3)
    
    return start_times, end_times


def threshold_activity(x, Tp, Ta):
    locs = scipy.signal.find_peaks(x,height = Tp)[0]
    y = (x > Ta) * 1
    act = np.diff(y)
    u = np.where(act == 1)[0]
    d = np.where(act == -1)[0]
    signal_length = len(x)
    
    if d[0] < u[0]:
        u = np.insert(u, 0, 0)
        
    if d[-1] < u[-1]:
        d = np.append(d, signal_length-1)
        
    starts = []
    ends = []
    
    activity = np.zeros(signal_length,)
    
    for candidate_up, candidate_down in zip(u, d):
        candidate_segment = range(candidate_up, candidate_down)
        peaks_in_segment = [x in candidate_segment for x in locs]
        is_valid_candidate = np.any(peaks_in_segment)
        if is_valid_candidate:
            starts.append(candidate_up)
            ends.append(candidate_down)
            activity[candidate_segment] = 1.0
            
    starts = np.array(starts)
    ends = np.array(ends)
    return activity, starts, ends
