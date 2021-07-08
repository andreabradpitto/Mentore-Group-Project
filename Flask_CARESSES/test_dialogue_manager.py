import requests
import os

# Location of the API (the server it is running on)
localhost = "127.0.0.1"
#azure_server = "13.95.222.73"
#cineca = "131.175.198.134"
#BASE = "http://" + cineca + ":5000/"
BASE = "http://" + localhost + ":5000/"

client_id = -1
if os.path.exists("credentials.txt"):
    with open("credentials.txt", 'r') as f:
        client_id = f.readline()
    print("Welcome back client", str(client_id), "!")
    print("R: I missed you. What would you like to talk about?")


def main():
    global client_id
    if client_id == -1:
        response = requests.put(BASE + "caresses/0/0", verify=False)
        client_id = response.json()['id']
        with open("credentials.txt", 'w') as credentials:
            credentials.write(str(client_id))
        print("Hey, you're new! Welcome, your ID is:", str(client_id))
        print("R:", response.json()['reply'])
    while 1:
        sentence = input("U: ")
        sentence = sentence.replace(" ", "_")
        response = requests.get(BASE + "caresses/" + str(client_id) + "/" + sentence, verify=False)
        # print("Response time: ", response.elapsed.total_seconds())
        intent_reply = response.json()['intent_reply']
        reply = response.json()['reply']
        plan = response.json()['plan']

        reply = intent_reply + " " + plan + " " + reply
        print("R:", reply)


if __name__ == '__main__':
    main()
