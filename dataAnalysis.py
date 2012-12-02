import struct
import numpy as np
import variables as var
import matplotlib.pyplot as mpp

def normalize(dictionnary):
    '''Normalize a dict so that the norm is 1'''
    total_norm = 0
    for(key, value) in dictionnary.items():
        total_norm += value**2
    for(key, value) in dictionnary.items():
        dictionnary[key] = value / np.sqrt(total_norm)
    return dictionnary

def getFft(data, rate):
    '''Get the FFT dictionnary of data with a sample of rate'''
    data=np.array(struct.unpack("%dB"%(var.CHUNK*4),data))
    fft_values = np.fft.fft(data)
    fft_frequencies = np.fft.fftfreq(var.CHUNK * 4 , 1.0/rate)
    fft_values = fft_values[1:]
    fft_frequencies = fft_frequencies[1:]
    
    res = {}
    for (i, freq) in enumerate(fft_frequencies):
        res[abs(freq)] = np.absolute(fft_values[i])

    return res

def distance(dict_1, dict_2):
    '''Get the distance between two normalized dictionnaries'''
    distance = 0
    for frequency in dict_1 :
        if frequency in dict_2 :
            distance += (dict_1[frequency] - dict_2[frequency]) ** 2
        else :
            print dict_1
            print dict_2
            distance += (dict_1[frequency] - dict_2[frequency]) ** 2

    return np.sqrt(distance)

def average_dictionary(dictionaries):
    '''average a list of dictionaries and returns a normalized version'''
    mean_dictionary = {}
    for fft_dictionnary in dictionaries :
       for (frequency, value) in fft_dictionnary.items() :
            if frequency in mean_dictionary :
                mean_dictionary[frequency] += value
            else :
                mean_dictionary[frequency] = value

    for frequency, value in mean_dictionary.items() :
        mean_dictionary[frequency] = value / len(dictionaries)

    return normalize(mean_dictionary)