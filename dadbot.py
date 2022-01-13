#!/usr/bin python3

# Created by Matthew Getgen
#   on 10-09-2021

# This program
import sys                          # for cl arguments
from PIL import Image               # for opening images (from PIL package)
import os                           # for system functions
import string                       # for removing punctuation >:]
import random                       # for choosing a random response ;)
import json                         # for json files :)

# heavy lifters
import speech_recognition as sr     # for speech recognition!
import pyttsx3                      # for speech to text!


def clearScreen():
    os.system('clear')


def showImageFullscreen(image_dir, image_name):
    im = Image.open(image_dir + image_name)
    im.show()


def dad_print(message):
    print(" > {}".format(message))


def dad_speak(message, voice_engine):
    dad_print(message)
    voice_engine.say(message)
    voice_engine.runAndWait()
    voice_engine.stop()


def choose_random(phraseList):
    return random.randint(0, len(phraseList)-1)
    
    
def make_response(phrases, key, words, index):
    if key == "im":
        blank = words[index+len(key):]
        return phrases["im"][0]+blank+phrases["im"][1]
    elif key == "thats":
        blank = words[index+len(key):]
        return phrases["thats"]+blank
    elif key == "money" or key == "hey" or key == "hello" or key == "goodbye":
        return phrases[key]
    elif key == "joke" or key == "can" or key == "why" or key == "random":
        rand = choose_random(phrases[key])
        return phrases[key][rand]
    else:
        return words


def find_keywords(keywords, words):
    for key in keywords:
        if key in words:
            # worry about only the first thing that matches.
            return key, words.find(key)
    return "random", 0


def recognize_speech(rec, mic):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(rec, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with mic as source:
        rec.adjust_for_ambient_noise(source)
        audio = rec.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcript": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #    update the response object accordingly
    try:
        response["transcript"] = rec.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unrecognizable
        response["error"] = "Unable to recognize speech"
    return response


def listen(rec, mic):
    words = recognize_speech(rec, mic)
    if words["error"] is not None and words["success"] is False:
        print("ERROR: {}".format(words["error"]))
        return False
    return words["transcript"]


def listen_input():
    return input("Say something: ")


def main():
    recognize_voice = 0
    image_dir = "./pictures/"

    with open("dad_phrases.json", "r") as phrase_file:
        phrases = json.load(phrase_file)
    
    if len(sys.argv) < 2:
        print('Arguments expected: <voice_recogniton> [0 or 1]')
        return
    else:
        if sys.argv[1] != "0":
            recognize_voice = 1
    
    if recognize_voice:
        # create recognizer and mic instance
        rec = sr.Recognizer()
        mic = sr.Microphone(device_index=6)     # system default microphone index = 6
        # for a look at different microphone devices, try:
        # print("\n",sr.Microphone.list_microphone_names())

        voice_engine = pyttsx3.init()   # object creation

        #   RATE
        voice_engine.setProperty('rate', 140)

        #   VOLUME
        voice_engine.setProperty('volume',1.0)

        #   VOICE
        voices = voice_engine.getProperty('voices')
        # index 10 for default male, 11 for english male
        voice_engine.setProperty('voice', voices[10].id)

    # showImageFullscreen(image_dir, "dad.jpg")
    # later, get a random image from a set of dad images, switching through them periodically
    # or  based on what the dad says.

    clearScreen()   # clears the microphone errors from ALSA lib. It's no big deal, but looks serious.
    if recognize_voice:
        dad_speak("Hello, I am Dad.", voice_engine)   # say through dad voice
    else:
        dad_print("Hello, I am Dad.")
    
    while 1:
        if recognize_voice:
            words = listen(rec, mic)
        else:
            words = listen_input()
        if words == False:
            return
    
        while words == None:
            if recognize_voice:
                words = listen(rec, mic)
            else:
                words = listen_input()
            if words == False:
                return
        
        # remove punctuation, for finding keywords
        new_w = words.lower()
        for c in string.punctuation:
            new_w = new_w.replace(c,"")
    
        keyword, index = find_keywords(phrases['keywords'], new_w)
        response = make_response(phrases, keyword, new_w, index)

        if recognize_voice:
            dad_speak(response, voice_engine)
        else:
            dad_print(response)

    return


if __name__ == '__main__':
    main()

"""
for tomorrow:
    say random phrases every few seconds inplementation, or if there is no keyword caught
    add more jokes, phrases, etc.
    add display different image implementation, might need a new library to do this how I want it
    have dad tell you goodnight.
    have dad greet you.
    clean up code
"""
