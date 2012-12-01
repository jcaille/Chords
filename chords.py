"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import struct
import numpy as np

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
wave_file = "/Users/jean/Devel/Chords/test.wav"
learning_file = "/Users/jean/Devel/Chords/learn.wav"

def getFft(data, rate):
    data=np.array(struct.unpack("%dB"%(CHUNK*4),data))
    fft_values = np.fft.fft(data)
    fft_frequencies = np.fft.fftfreq(CHUNK * 4 , 1.0/rate)
    fft_values = fft_values[1:]
    fft_frequencies = fft_frequencies[1:]
    
    res = {}
    for (i, freq) in enumerate(fft_frequencies):
        res[abs(freq)] = np.absolute(fft_values[i])

    return res

def normalize(dictionnary):
    total_norm = 0
    for(key, value) in dictionnary.items():
        total_norm += value**2
    for(key, value) in dictionnary.items():
        dictionnary[key] = value / np.sqrt(total_norm)
    return dictionnary

def learn(learning_data):
    print "Learning"
    wf = wave.open(learning_data, 'rb')
    dicitonnaries = []
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        # stream.write(data)
        dicitonnaries.append(getFft(data, wf.getframerate()))
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

    # Average the dictionary
    mean_dictionnary = {}
    for fft_dictionnary in dicitonnaries :
        for (frequency, value) in fft_dictionnary.items() :
            if frequency in mean_dictionnary :
                mean_dictionnary[frequency] += value
            else :
                mean_dictionnary[frequency] = value

    for frequency, value in mean_dictionnary.items() :
        mean_dictionnary[frequency] = value / len(dicitonnaries)

    mean_dictionnary = normalize(mean_dictionnary)
    print "Done Learning"
    
    threshold = 0
    count = 0
    wf = wave.open(learning_data, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        count += 1
        threshold += getDistance(data, wf.getframerate(), mean_dictionnary)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

    threshold /= count
    threshold *= 1.5

    print "Done setting the threshold at " + str(threshold)
    return mean_dictionnary, threshold


def getDistance(data, rate, ref_dictionnary):
    data_dictionnary = normalize(getFft(data, rate))
    distance = 0
    for frequency in data_dictionnary :
        distance += (ref_dictionnary[frequency] - data_dictionnary[frequency]) ** 2
    return np.sqrt(distance)

def compare(sample_file, ref_dictionnary, threshold):
    wf = wave.open(sample_file, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True)

    data = wf.readframes(CHUNK)
    i = 0

    while data != '':
        i += 1
        stream.write(data)
        if i%8 == 0 :
            distance = getDistance(data, wf.getframerate(), ref_dictionnary)
            if(distance < threshold):
                print "MAAAATCH"
            else :
                print ":("
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def liveCompare(ref_dict, threshold) :
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    i = 0
    while(True):
        data = stream.read(CHUNK)
        i += 1
        if i%5 == 0 :
            distance = getDistance(data, RATE, ref_dict)
            if(distance < threshold):
                print "MAAAATCH"
            else :
                print ":("
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

def main(argv=None) :
    ref_dictionnary, threshold = learn(learning_file)
    liveCompare(ref_dictionnary, threshold)

main()