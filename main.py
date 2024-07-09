#pip install speechrecognition
#pip install wikipedia
#pip install openai
#pip install pyaudio
#pip install win32com.client
#pip install webbrowser
# pip install setuptools

import openai
from apikey import key  # Assuming 'apikey.py' contains your OpenAI API key
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import win32com.client
import subprocess

# Initialize text-to-speech
speaker = win32com.client.Dispatch("SAPI.SpVoice")
voices = speaker.GetVoices()
speaker.Voice = voices[1]  # Change index to switch between male (0) and female (1) voices

# Function to speak aloud
def talk(text):
    print(text, end="\n")  # Print text to console
    speaker.Speak(text)    # Speak text aloud

# Function to listen to user's voice input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')  # Recognize speech using Google Speech Recognition
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            talk("Say that again please...")  # Ask user to repeat if speech is not recognized
            return "None"
    return query

# Function to interact with OpenAI's chat API (requires API key)
def ai(query):
    openai.api_key = key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ]
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.RateLimitError:
        return "Sorry, this feature is unavailable due to insufficient balance."
    
def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        talk(f"Failed to run the script: {script_path}. Error: {e}")
    except Exception as e:
        talk(f"An error occurred: {e}")    

# Main function for conversational interactions
if __name__ == "__main__":
    talk("Hello! I am Shinchan, your A.I assistant.")
    talk("How can I help you?")
    while True:
        query = listen()  # Listen for user input
        # List of predefined sites and apps to open based on user input
        sites = [
            ['youtube', 'https://www.youtube.com'], 
            ['google', 'https://www.google.com'], 
            ['github', 'https://github.com'], 
            ['notes', 'https://keep.google.com'], 
            ['linked', 'https://www.linkedin.com'], 
            ['instagram', 'https://www.instagram.com']
        ]
        apps = [
            ['discord', r'Location of discord app'], 
            ['epic games', r'Location of epic games app']
        ]
        
        # Check if user query matches predefined apps or sites to open
        for app in apps:
            if app[0] in query.lower():
                os.startfile(app[1])  # Open the specified application
                talk(f"Opening {app[0]}")
                exit()
        
        for site in sites:
            if site[0] in query.lower():
                talk("Opening " + site[0])
                webbrowser.open(site[1])  # Open the specified website
                exit()

        # Handle Wikipedia search
        if 'wikipedia'.lower() in query.lower():
            talk('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()  # Remove "wikipedia" and strip leading/trailing spaces
            # query = urllib.parse.quote(query)  # URL encode the query
            try:
                results = wikipedia.page(title=query, auto_suggest=True)
                webbrowser.open(results.url)
            except wikipedia.exceptions.DisambiguationError as e:
                try:
                    results = wikipedia.page(e.options[0], auto_suggest=True)
                    webbrowser.open(results.url)
                except wikipedia.exceptions.PageError as e:
                        talk(f"Sorry, I couldn't find any results for {query}.")
            except wikipedia.exceptions.PageError as e:
                try:
                    query = '_'.join(query.split())
                    webbrowser.open(f'https://en.wikipedia.org/wiki/{query}')
                except wikipedia.exceptions.PageError as e:
                        talk(f"Sorry, I couldn't find any results for {query}.")   
            break    
        
        # Handle opening local folders
        elif 'open folder'.lower() in query.lower():
            talk('Which folder do you want to open?')
            folder_name = input("Enter full address of the folder: ")
            os.startfile(folder_name)

        # Respond to queries about current time and date
        elif 'the date and time'.lower() in query.lower():
            path = r'Path of today.py'
            run_script(path)

        # Handle chat with OpenAI (requires API key)
        elif 'using chat'.lower() in query.lower():
            query = query.replace("using chat", "")
            ans = ai(query)
            print(ans)

        elif 'activate'.lower() in query.lower():
            talk("Badabadabadabada")

        elif 'the weather'.lower() in query.lower():
            script_path = r"Location of weather.py"
            run_script(script_path)

        elif 'the news'.lower() in query.lower():
            script_path = r"Location of news.py"
            run_script(script_path)

        # Exit the assistant
        elif 'sleep'.lower() in query.lower():
            talk("Thanks for using me, see you soon")
            break
        
        # For all other queries, use OpenAI for a response
        else:
            ans = ai(query)
            talk(ans)
