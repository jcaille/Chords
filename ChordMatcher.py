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
        last_match = -1
        challenger = -1
        successive_challenge = 0
        while(True):
            try: 
                  data = stream.read(var.CHUNK) 
            except IOError: 
                  pass 

            i += 1
            if i%2 == 0 :
                data_fft = da.normalize(da.getFft(data, var.RATE))
                best_match, distance_to_best_match = self.match(data_fft)
                if last_match == -1 :
                    last_match = best_match
                    print "I got " + best_match.name + " with an error of " + str(distance_to_best_match)
                else :
                    if last_match != best_match :
                        # distance_to_last_match = da.distance(data_fft, last_match.chord_fft)
                        if best_match == challenger or challenger == -1 :
                            successive_challenge += 1
                            if successive_challenge > 3 :
                                print "I got " + best_match.name + " with an error of " + str(distance_to_best_match)
                                last_match = best_match
                                challenger = -1
                                successive_challenge = 0
                            else :
                                # print "o"
                                pass
                        else :
                            # print "x"
                            challenger = best_match 
                            successive_challenge = 0
                    else :
                        # print "."
                        challenger = -1
                        successive_challenge = 0



        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()