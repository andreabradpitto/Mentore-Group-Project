import requests

# Location of the API (the server it is running on)
#localhost = "127.0.0.1"
#azure_server = "13.95.222.73"
cineca = "131.175.198.134"
BASE = "http://" + cineca + ":5001/"
#BASE = "http://" + localhost + ":5001/"

def main():
    topic_n = 0
    sentence = input("Sentence: ")
    sentence = sentence.replace(" ", "_")
    response = requests.get(BASE + "regex_match/" + str(topic_n) + "/" + sentence, verify=False)
    print(response.json())
    #print("Extracted parameters:", response.json()['parameters'])
    #print("Parameters type:", response.json()['type'])


if __name__ == '__main__':
    main()
