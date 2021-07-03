import requests
import os
import pyttsx3
import speech_recognition as sr





# Location of the API (the server it is running on)
localhost = "127.0.0.1"
#azure_server = "13.95.222.73"
#cineca = "131.175.198.134"
BASE = "http://" + localhost + ":5000/"

client_id = -1
if os.path.exists("credentials.txt"):
    with open("credentials.txt", 'r') as f:
        client_id = f.readline()
    print("Welcome back client", str(client_id), "!")
    print("R: I missed you. What would you like to talk about?")
    engine = pyttsx3.init()
    
    text = "Welcome back client", str(client_id)
    text1 = "I missed you. What would you like to talk about?"


                         
    voices = engine.getProperty('voices')                         
    engine.setProperty('volume',5.0)
    engine.setProperty('voice', voices[1].id)
    
    engine.setProperty("rate", 165)
    engine.say(text)
    engine.say(text1)
    engine.runAndWait()



def main():
    global client_id
    if client_id == -1:
        response = requests.put(BASE + "caresses/0/0", verify=False)
        client_id = response.json()['id']
        with open("credentials.txt", 'w') as credentials:
            credentials.write(str(client_id))
        print("Hey, you're new! Welcome, your ID is:", str(client_id))
        print("R:", response.json()['reply'])
        intro = pyttsx3.init()
        intro_text = "Hey, you're new! Welcome, your ID is:", str(client_id)
        intro_text1 = "R:", response.json()['reply']
        intro.setProperty('voice', voices[1].id)
        intro.setProperty("rate", 165)
        intro.say(intro_text)
        intro.runAndWait()
        intro.say(intro_text1)
        intro.runAndWait()
    while 1:
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak Anything :")
            audio = r.listen(source)
            try:
                texta = r.recognize_google(audio)
                print("You said : {}".format(texta))
            except:
                print("")
        #sentence = input("U: ")
        sentence = texta
        sentence = sentence.replace(" ", "_")
        response = requests.get(BASE + "caresses/" + str(client_id) + "/" + sentence, verify=False)
        # print("Response time: ", response.elapsed.total_seconds())
        intent_reply = response.json()['intent_reply']
        reply = response.json()['reply']
        plan = response.json()['plan']

        reply = intent_reply + " " + plan + " " + reply
        print("R:", reply)
        
        
        reply_t = pyttsx3.init()
        reply_text = reply
        reply_t.setProperty('voice', voices[1].id)
        reply_t.setProperty("rate", 165)
        reply_t.say(reply_text)
        reply_t.runAndWait()

        
        


if __name__ == '__main__':
    main()
