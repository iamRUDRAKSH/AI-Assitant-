import win32com.client 
speaker = win32com.client.Dispatch("SAPI.SpVoice") 
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='da98e145e4914327a914f88e934054e0')

speaker.Speak("Hello! This is News Assistant.")
print("Press 0 for sports news.")
print("Press 1 for business news.")
print("Press 2 for tech news.")
print("Press 3 for entertainment news.")
print("Press 4 for general news.")
print("Press 5 to quit.")

while True:
    ans = int(input("Your response : "))
    if ans == 5:
        break
    cat_list = ['sports', 'business', 'technology', 'entertainment', 'general']
    cat = cat_list[ans]
    headlines = newsapi.get_top_headlines(
                                          category = cat,
                                          language = 'en',
                                          country = 'in')
    count = 1
    for headline in headlines['articles']:
        if count == 6:
            break
        speaker.Speak(f"News {count}")    
        print(headline['title'])
        speaker.Speak(headline['title'])
        print(headline['description'])
        print("-----------------------------------------------------------------------------------")
        count += 1





