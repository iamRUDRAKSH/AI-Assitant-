#pip install speechrecognition
#pip install wikipedia
#pip install openai
#pip install pyaudio
#pip install win32com.client
#pip install webbrowser
# pip install setuptools

import google.generativeai as genai
from apikey import key  # Assuming 'apikey.py' contains your OpenAI API key
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import win32com.client
import subprocess
from playwright.sync_api import sync_playwright

genai.configure(api_key=key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

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
    response = model.generate_content(query)
    print(response.text)
    return response.text
    
def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the script: {script_path}. Error: {e}")
    except Exception as e:
        talk(f"An error occurred: {e}")

def play(video):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto("https://www.youtube.com/")
            page.wait_for_timeout(3000)  # Wait for the page to load

                # Locate the search input field and fill it with thevideo name
            search_input = page.locator('//input[@id="search"]')
            search_input.click()
            search_input.fill(video)
            page.wait_for_timeout(1000)

                # Press Enter to search for thevideo
            page.keyboard.press('Enter')
            page.wait_for_timeout(3000)

                # Click the first video in the search results
            first_video = page.locator('//a[@id="video-title"]')
            first_video.first.click()
            page.wait_for_timeout(5000)
                
            while True:
                page.wait_for_timeout(1000)

        except Exception as e:
            print("Browser closed.")

def chat():
    chat_session = model.start_chat(
        history=[]
    )
    while True:
        query = listen()
        if query == "None":
            continue
        elif "exit" or "quit" in query.lower():
            talk("Goodbye!")
            break
        elif "clear" in query.lower():
            chat_session.history = []  # Clear the history list
            talk("Chat history cleared.")
            continue
        response = chat_session.send_message(query)
        talk(response.text)


# Main function for conversational interactions
if __name__ == "__main__":
    talk("Hello! I am bot.")
    talk("How may I help you?")
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
            ['discord', r'Address of app'], 
            ['epic games', r'Address of app']
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
            path = r'Address of today.py'
            run_script(path)

        # Handle chat with OpenAI (requires API key)
        elif 'chat'.lower() in query.lower():
            chat()

        elif 'activate'.lower() in query.lower():
            talk("Badabadabadabada")

        elif 'the weather'.lower() in query.lower():
            script_path = r"Address of weather.py"
            run_script(script_path)

        elif 'the news'.lower() in query.lower():
            script_path = r"Address of news.py"
            run_script(script_path)

        elif 'play' in query.lower():
            video = query.split('play')[1].strip()
            talk('Playing ' + video)
            play(video)

        # Exit the assistant
        elif 'sleep'.lower() in query.lower():
            talk("Thanks for using me, see you soon")
            break
        
        # For all other queries, use OpenAI for a response
        else:
            ans = ai(query)