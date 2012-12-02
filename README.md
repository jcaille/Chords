Chords
======

Python script that recognizes chords from a guitar.
Uses numpy and pyaudio

How to use
=====
* Install dependencies : Numpy and Pyaudio
* Use record.py to record short sound snippets and name them accordingly
* In chords.py, use learn_from_audio to extract the information from your snippets once and for all (it saves them in pickled files in the reference folder)
* In chords.py, use live_recognition to launch
