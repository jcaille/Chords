import pyaudio
import wave
import dataAnalysis as da
import variables as var
import pickle

class ReferenceSnippet() :
    def __init__(self, name="None") :
        self.chord_fft = {}
        self.threshold = 0
        self.name = name

    def learn_from_wave_file(self, file_path) :
        print "Learning"
        wf = wave.open(file_path, 'rb')
        dictionaries = []
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        data = wf.readframes(var.CHUNK)

        while data != '':
            dictionaries.append(da.getFft(data, var.RATE))
            data = wf.readframes(var.CHUNK)

            stream.stop_stream()
            stream.close()


        # Average the dictionary
        mean_dictionnary = da.average_dictionary(dictionaries)
        print "Done Learning" 
        
        threshold = 0
        count = 0
        wf = wave.open(file_path, 'rb')

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        data = wf.readframes(var.CHUNK)

        while data != '':
            count += 1
            data_fft = da.normalize(da.getFft(data, wf.getframerate()))
            threshold += da.distance(data_fft, mean_dictionnary)
            data = wf.readframes(var.CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()

        threshold /= count

        print "Done setting the threshold at " + str(threshold)
        self.chord_fft = mean_dictionnary
        self.threshold = threshold

    def save_to_file(self, f):
        print ("Saving to file " +f)
        my_file = open(f, 'w')
        compressed_form = {"name" : self.name, "threshold" : self.threshold, "fft_data" : self.chord_fft}
        pickle.dump(compressed_form, my_file)
        my_file.close()

    def load_from_file(self, f):
        my_file = open(f, 'r')
        compressed_form = pickle.load(my_file)
        my_file.close()

        self.chord_fft = compressed_form["fft_data"]
        self.threshold = compressed_form["threshold"]
        self.name = compressed_form["name"]