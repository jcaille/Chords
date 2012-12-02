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
        print "Learning for "+ self.name
        wf = wave.open(file_path, 'rb')
        dictionaries = []
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        data = wf.readframes(var.CHUNK)

        while data != '':
            dictionaries.append(da.normalize(da.getFft(data, var.RATE)))
            data = wf.readframes(var.CHUNK)

            stream.stop_stream()
            stream.close()


        # Average the dictionary
        mean_dictionnary = da.average_dictionary(dictionaries)
        print "Done Learning" 
        
        threshold = 0 ;
        for fft_data in dictionaries :
            threshold += da.distance(fft_data, mean_dictionnary)

        threshold /= len(dictionaries)

        print "Done setting the threshold at " + str(threshold)

        real_list = []
        for fft_data in dictionaries :
            if da.distance(fft_data, mean_dictionnary) < threshold :
                real_list.append(fft_data)

        new_mean = da.average_dictionary(real_list)
        print "Done filtering"
        print "Distance between the new and old means is " + str(da.distance(mean_dictionnary, new_mean))

        threshold = 0 ;
        for fft_data in real_list :
            threshold += da.distance(fft_data, new_mean)

        threshold /= len(real_list)
        print "Done resetting the threshold at " + str(threshold)
        print len(real_list)
        self.chord_fft = new_mean
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