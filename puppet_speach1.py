#!/usr/bin/python3

# this worked on Linux machine. does it work on Raspi?
import os
os.system("espeak 'Hello I am a puppet. Who are you?'")


# this doesn't work. eSpeak is installed at a system level so maybe it isn't a library to import?
# maybe this will work differently on the RasPi?

# one comment says:

# There is no python module called espeak.
# You dont need it, just make sure you've installed espeak
# on your distribution and you can do it with subprocess calls.
#from espeak import espeak as esp

text = 'Hello I am a puppet. Who are you?'
#esp.says(text)
#esp.synth(text)

# copied from
# https://www.devdungeon.com/content/text-speech-pysthon-pyttsx3
# this works iff easyspeak already installed

import pyttsx3

# One time initialization
engine = pyttsx3.init()

# Set properties _before_ you add things to say
engine.setProperty('rate', 130)    # Speed percent (can go over 100)
engine.setProperty('volume', 0.9)  # Volume 0-1

# Queue up things to say.
# There will be a short break between each one
# when spoken, like a pause between sentences.
engine.say(text)
#engine.say("You can queue up multiple items")

# Flush the say() queue and play the audio
engine.runAndWait()

# Program will not continue execution until
# all speech is done talking
