import datetime as dt
import speech_recognition as sr
import pyttsx3 as tts
import wikipedia as wiki
import pyjokes as pj
import webbrowser as browser
import requests
import openweather as pyowm
import urllib
import re

from wikipedia.wikipedia import random
owkey = 'af74a38c175d420e6b4fab8313401c87'

recognizer = sr.Recognizer()
microphone = sr.Microphone()

engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('voice', voices[1].id)

class pyAssist:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def greet(self):
        engine.say('How can I help you?')
        engine.runAndWait()

    def trigger(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print('Listening...')

                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    voice = recognizer.listen(source, timeout = 5.0)
                    response = recognizer.recognize_google(voice)
                    response = response.lower()

                    if 'inday' in response:
                        return response
                    else:
                        pass     
                          
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))  

    def listen(self, recognizer, microphone, response):
        try:
            with microphone as source:
                p.talk('Inday is here')
                print('Waiting...')

                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                voice = recognizer.listen(source, timeout = 5.0)
                command = recognizer.recognize_google(voice)
                command = command.lower()

                print("Command: " + command)
                return command
                
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))  
       
    def talk(self, text):
        engine.say(text)
        engine.runAndWait()

    def ai(self, command):
        try:
            if 'who are you' in command:
                p.talk('I am inday. I am your virtual assistant')
            elif 'how are you' in command:
                feels = ["I'm okay.", "I'm doing well.", "Feels great."]
                greet = random.choice(feels)
                p.talk(greet)
                print(greet)
            elif 'search' in command:
                search = command.replace('search', '')               
                result = wiki.summary(search, 1)
                p.talk(result)
                print(result)
            elif 'play' or 'youtube' in command:
                p.get_youtube(command)
            elif 'time' in command:
                time = dt.datetime.now().strftime('%I:%M %p')
                p.talk('It is ' + time)
                print(time)
            elif 'today' in command:
                today = dt.datetime.now().strftime('%B %d, %Y')
                p.talk('Today is ' + today)
                print(today)
            elif 'joke' in command:
                joke = pj.get_joke()
                p.talk(joke)
                print(joke)
            elif 'weather' in command:
                p.get_weather(command)
            else:
                p.talk('Not yet available.')
        except TypeError as te:
            print(te)
            pass
        except AttributeError as ae:
            print(ae)
            pass

    def get_youtube(self, command):
        if 'play' in command:
            keyword = command.replace('play', '')
            short_keyword = keyword.replace(' ', '')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + short_keyword)
            ytid = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            browser.open("https://www.youtube.com/watch?v=" + ytid[0])
            p.talk('Playing' + keyword)
        else:
            p.talk('This is still in development.')

    def get_weather(self, command):
        home = 'Oroquieta City'
        owm = pyowm(owkey)
        weather_mgr = owm.weather_manager()
        
        if 'now' in command:
            obs = weather_mgr.weather_at_place(home)
            weather = obs.weather

            temp = weather.temperature('celsius')
            status = weather.status
            p.talk('It is currently' + str(int(temp['temp'])) + 'degrees and' + status)
        else:
            p.talk('This is still in development.')

    # def get_weather(self, command):
    #     key = owkey
    #     base_url = 'http://api.openweathermap.org/data/2.5/weather?&q='
    #     city_name = 'Oroquieta City'
    #     units = 'metric'

    #     final_url = base_url + city_name + '&units=' + units + 'appid=' + key
    #     weather_data = requests.get(final_url).json()
    #     print(weather_data)

    #     if 'now' in command:
    #         temperature = weather_data['main']['temp']
    #         status = weather_data['weather'][0]['description']
    #         p.talk('It is currently ' + temperature + 'degrees and ' + status )
    #         print(temperature)
    #         print(status)
    #     else:
    #         p.talk('Could not get weather info')

p = pyAssist()

while True:
    response = p.trigger(recognizer, microphone)
    command = p.listen(recognizer, microphone, response)
    p.ai(command)
    