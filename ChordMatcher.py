import dataAnalysis as da
import pyaudio
import variables as var

class ChordMatcher():
    def __init__(self, chords) :
        self.chords = chords
        print(len(self.chords))

    def match(self, data_fft) :
        min_distance = da.distance(self.chords[0].chord_fft, data_fft)
        best_match = self.chords[0]
        for chord in self.chords :
            current_distance = da.distance(chord.chord_fft, data_fft)
            if current_distance < min_distance :
                best_match = chord
                min_distance = current_distance

        return best_match, min_distance

    def listen(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=var.CHANNELS,
                        rate=var.RATE,
                        input=True,
                        frames_per_buffer=var.CHUNK)

        print("* recording * ")

        data = stream.read(var.CHUNK)

        i = 0
        successive_match = 0
        last_match = -1
        challenger = -1

        while(True):
            data = stream.read(var.CHUNK)
            i += 1
            if i%5 == 0 :
                data_fft = da.normalize(da.getFft(data, var.RATE))
                best_match, distance_to_best_match = self.match(data_fft)
                if last_match != -1 :
                    distance_to_last_match = da.distance(data_fft, last_match.chord_fft)
                else :
                    distance_to_last_match = 10

                if best_match == last_match :
                    if distance_to_best_match > best_match.threshold * 2 :
                        print "I got nothing"
                        last_match = -1                
                else :
                    if distance_to_best_match < distance_to_last_match * 0.9 :
                        if distance_to_best_match < best_match.threshold * 1.2 :
                            if successive_match > 1 :
                                print "I got " + best_match.name + " with an error of " + str(distance_to_best_match)
                                last_match = best_match 
                            else :
                                if best_match == challenger :
                                    successive_match += 1
                                else :
                                    print "Challenger Beaten by " + best_match.name
                                    challenger = best_match
                                    successive_match = 0

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()