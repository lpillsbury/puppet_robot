#!/usr/bin/python3

import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 130)    # Speed percent (can go over 100)
engine.setProperty('volume', 0.9)  # Volume 0-1
r = sr.Recognizer()

text = 'what is your name'
engine.say(text)
yourname = sr.AudioFile('name_input.wav')
with yourname as source:
    audio = r.record(source)
name = r.recognize_google(audio)

engine.say(name)

engine.runAndWait()
