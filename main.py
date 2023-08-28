import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pyautogui
import os
import openai
from time import sleep

# Creating a recognizer who can understand audio input
listener = sr.Recognizer()

# initialize text to speech (TTS) object 
engine = pyttsx3.init()

# Change the voice from male to female
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# function for TTS output
def talk(text):
    engine.say(text)
    engine.runAndWait()

# AI introduces itself using TTS API
talk("Hello, what can I do for you?")

# openAI function for generating response from given prompt
def AI(prompt):

    # Create and retrieve openAI API key from .env file
    OPENAI_KEY = os.getenv(API_KEY)
    openai.api_key = OPENAI_KEY
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # openAI returns a list called choices - I only want the text response that comes from it 
    return response.choices[0].text

# function for accepting a command and returning it 
def take_command():
    try:
        # calling microphone as source 
        with sr.Microphone() as source:
            print("Listening...")
            # asking the speech recognizer (listener) to listen to the source (microphone)
            voice = listener.listen(source)
            # using speech recognition API to convert the audio into a string 
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                command = command.replace("alexa", "")
                print(command)

    # catch any/all of the exceptions that can possibly be thrown 
    except Exception:
        print("An unknown error has occured")

    return command

# function for processing command from user 
def run_assistant():
    command = take_command()
    if "play the song" in command:
        song = command.replace("play the song", "")
        # open the spotify web player
        webbrowser.open(f"https://open.spotify.com/search/{song}")
        # telling the computer to wait x seconds before pressing (so the page can load)
        sleep(6)
        # click on the play button that correspond to the given coordinates
        pyautogui.click(x = 800, y = 480)
        talk("playing" + song)
    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        talk("The current time is " + time)
    elif "artificial intelligence" in command:
        response = AI(command)
        print(response)
        talk(response)
    elif "thank you, that is all" or "thank you" in command:
        exit()

# run the function so that the code executes/prompts more than once
while True:
    run_assistant()