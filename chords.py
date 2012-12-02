import referenceSnippet as rs
import ChordMatcher as cm
import variables as var
import os

# Learn several chords and store them somewhere
 
def learn_from_audio_files() :
    files_to_learn = []
    for files in os.listdir(var.audio_files_folder):
        if files.endswith(".wav"):
            files_to_learn.append(files)

    snippets = []
    for wave_file in files_to_learn :
        name = wave_file[0:-4]
        real_file = var.audio_files_folder + wave_file
        snippet = rs.ReferenceSnippet(name)
        snippet.learn_from_wave_file(real_file)

        pickle_file = var.reference_folder + name +".crd"
        snippet.save_to_file(pickle_file)
        snippets.append(snippet)

    return snippets

def retrieve_snippets() :
    files_to_retrieve = []
    for files in os.listdir(var.reference_folder):
        if files.endswith(".crd"):
            files_to_retrieve.append(files)

    snippets = []
    for chord_file in files_to_retrieve :
        snippet = rs.ReferenceSnippet()
        snippet.load_from_file(var.reference_folder + chord_file)
        snippets.append(snippet)

    return snippets

def live_recognition() :
    chords = retrieve_snippets()
    matcher = cm.ChordMatcher(chords)
    matcher.listen()

# learn_from_audio_files()
live_recognition()