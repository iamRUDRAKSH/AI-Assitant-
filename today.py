import time
import win32com.client 
speaker = win32com.client.Dispatch("SAPI.SpVoice")


day = time.strftime('%A %d %B %Y')
hour = int(time.strftime('%H'))
minute = int(time.strftime('%M'))
speaker.Speak( "it's" + day)
print(day)
speaker.Speak(f"Time is {hour}:{minute}")
print(f"{hour}:{minute}")


date = int(time.strftime('%d'))
month = int(time.strftime('%m'))           

if(date == 18 and month == 4):
    speaker.Speak("Happy Birthday Sir!!")


if(hour >= 22 or hour < 5):
    speaker.Speak("Good night sir!!")
    speaker.Speak("Time to sleep.")
elif(hour >= 5 and hour < 12):
    speaker.Speak("Good morning sir!!")
elif(hour >= 12 and hour < 17):
    speaker.Speak("Good afternoon sir!!")
else:
    speaker.Speak("Good eveneing sir!!")
