import pandas as pd
import numpy as np
import os
import librosa
from pydub import AudioSegment

# read in wav file, get out signal (np array) and sampling rate (int)
def read_in_audio(filename):
    (sig, rate) = librosa.load(filename)
    return sig, rate

# get standard lenth audio file
def get_std_len_signal(filename):
    signal, rate = read_in_audio(filename)
    signal = signal[0:int(3.5 * rate)]  # Keep the first 3.5 seconds
    return signal, rate

# make mfcc np array from wav file using librosa package
def make_librosa_mfcc(signal, sr):
    mfcc_feat = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
    return mfcc_feat

# Get normalized mfcc features
def make_normed_mfcc(x):
    normed_mfcc = (x - np.mean(x))/np.std(x)
    normed_mfcc_feat = normed_mfcc.T
    return np.mean(normed_mfcc_feat, axis=0)

# # for folder containing wav files, output numpy array of normed mfcc
# def make_mfcc_df(folder):
#     lst = []
#     for filename in os.listdir(folder):
#         signal, rate = get_std_len_signal('./{}/{}'.format(folder,filename))
#         mfcc = make_librosa_mfcc(signal, rate)
#         normalized_mfcc = make_normed_mfcc(mfcc)
#         lst.append(normalized_mfcc)
#     mfcc_df = pd.DataFrame(lst)
#     return mfcc_df

# for folder containing wav files, output numpy array of normed mfcc
def make_mfcc(filename):
    signal, rate = get_std_len_signal('./wav/{}'.format(filename))
    mfcc = make_librosa_mfcc(signal, rate)
    normalized_mfcc = make_normed_mfcc(mfcc)
    mfcc_lst = list(normalized_mfcc)
    return mfcc_lst