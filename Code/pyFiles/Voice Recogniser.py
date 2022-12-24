#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pyttsx3
import speech_recognition as sr
from datetime import datetime
import wikipedia
import webbrowser
import os
import sys
sys.path.insert(0, 'C:/Users/puppa/Documents/Python Files/Basic Voice Assistant/Code/pyFiles')

from MovieRecom import movie_recommender
from BookRecom import book_recommender

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

class VoiceRecogniser:
    
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
    
    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    # print(voices)

    def wishMe(self, name):
        hour = int(datetime.now().hour)
        if hour>=0 and hour<12:
            self.speak(f"Good Morning! {name}")
        elif hour>=12 and hour<18:
            self.speak(f"Good Afternoon! {name}")  
        else:
            self.speak(f"Good Evening! {name}")  
        # speak("I am Anand. Please tell me how may I assist you")      

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.record(source,duration=5)
        try:
            print("Recognizing...")    
            query = r.recognize_google(audio,language='en-in')
            print(f"User said: {query}\n")
            #ok=1
        except Exception as e:
            self.speak("Say that again please...")
            return self.takeCommand()
            # return None
        return query

    def Movie_Recommenders(self):

        self.speak('Search for any similar Movie?')
        print('Search for any similar Movie?')

        q = self.takeCommand().lower()
        if 'go back' in q:
            return
        if 'yes' in q or 'yeah' in q:
            self.speak('Tell Movie Name')
            print('Tell Movie Name')
            mov_name = self.takeCommand().lower()
            # ok=1
            recom_movies = movie_recommender(mov_name)
            print('Recommended Movies for:'+str(mov_name))
            self.speak('Recommended Movies for'+str(mov_name))
            print(recom_movies)
        elif 'no' in q or 'nope' in q:
            recom_movies = movie_recommender()
            print('Recommended movies are:')
            self.speak('Recommended movies are')
            # ok=1
            print(recom_movies)
    #     if ok==0:
    #         Movie_Recommenders(1)
        return

    def Book_Recommenders(self):

        self.speak('Search for any similar Book?')
        print('Search for any similar Book?')

        q = self.takeCommand().lower()

        if 'go back' in q:
            return
        if 'yes' in q or 'yeah' in q:
            self.speak('Tell Book Name')
            print('Tell Book Name')
            bk_name = self.takeCommand().lower()
            book_recom = book_recommender(bk_name)
            print('Recommended Books for:'+str(bk_name))
            self.speak('Recommended Books for'+str(bk_name))
            for book in book_recom:
                print(book)
        elif 'no' in q or 'nope' in q:
            book_recom = book_recommender()
            print('Recommended Books are:')
            self.speak('Recommended books are')
            for book in book_recom:
                print(book)
    #     if ok==0:
    #         Book_Recommenders(1)
        return

    #_name_="main"
    def voice_assistant(self):

        self.speak("Hey! I'm Lee. Please tell me how may I assist you")
        self.speak("Before starting, please tell your name")
        name = self.takeCommand().lower()
        self.wishMe(name)

        while True:
            query = self.takeCommand().lower()
            # query = query.lower()
            # query = "open google"
            if 'wikipedia' in query:
                self.speak('Searching Wikipedia...')
                #query = query.replace("wikipedia", "")
                sub_query = self.takeCommand().lower()
                results = wikipedia.summary(sub_query, sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
            elif 'youtube' in query:
                self.speak('Searching youtube ...')
                webbrowser.open("youtube.com")
            elif 'google' in query:
                self.speak('Searching google ...')
                webbrowser.open("google.com")
            elif 'firefox' in query:
                self.speak('Searching firefox ...')
                webbrowser.open("firefox.com")
            elif 'hi' in query:
                self.speak('Hey! , What\'s up?')
            elif 'stackoverflow' in query:
                self.speak('Searching stackoverflow ...')
                webbrowser.open("stackoverflow.com")
            elif ('music' in query) or ('songs' in query) or ('song' in query):
                music_dir = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Songs'
                songs=os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir,songs[0]))
            elif 'exit' in query or 'quit' in query:
                print('Thank you, see you again, have a good day')
                self.speak('Thank you, see you again, have a good day')
                return
            elif 'who are you' in query:
                self.speak('Im Lee, the Voice assistant!')
            elif 'time' in query:
                strTime = datetime.now().strftime("%H:%M:%S")
                self.speak(f"the time is {strTime}")
            elif 'date' in query or 'day' in query:
                time = datetime.now()
                week, day, month, yr = time.strftime('%A'), time.day, time.month, time.year
                mapped_month = {
                    1: "January",
                    2: "February",
                    3: "March",
                    4: "April",
                    5: "May",
                    6: "June",
                    7: "July",
                    8: "August",
                    9: "September",
                    10: "October",
                    11: "November",
                    12: "December"
                }
                self.speak(f"It's {week} {day} of {mapped_month[month]}, {yr}")
            elif 'powerpoint' in query:
                codePath = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint"
                os.startfile(codePath)
            elif 'notepad' in query:
                codePath = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Notepad"
                os.startfile(codePath)
            elif 'zoom' in query:
                self.speak('opening zoom')
                webbrowser.open("zoom.com")
            elif 'facebook' in query:
                self.speak('opening facebook')
                webbrowser.open("facebook.com")
            elif ('instagram' in query) or ('insta' in query):
                self.speak('opening Instagram')
                webbrowser.open("instagram.com")
            elif 'recommend' in query or 'suggest' in query:
                if 'book' in query:
                    self.Book_Recommenders()
                elif 'movie' in query:
                    self.Movie_Recommenders()

if __name__ == "__main__":
    VoiceRecogniser().voice_assistant()


# In[ ]:




