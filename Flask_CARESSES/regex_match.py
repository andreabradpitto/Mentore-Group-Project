import re
import random
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


# This function returns a dictionary of dictionary:
# {'intent':{'t': [regexes], 'r': [replies], 'k': [kbplans], 'p': [plans]}, 'intent1':{...}, ...}
def get_common_intents():
    with open("F:\Robotics\Group_Project\BeingAI\Flask_CARESSES\dialogue_tree\common_intents.txt", 'r') as f:
        lines = f.readlines()

    common_ints = {}
    prev_intent = ''
    prev_str_type = ''
    for line in lines:
        # If the line begins with an underscore, process the regex
        if line[0] == '_':
            intent = line.split('_')[1]
            str_type = line.split('_')[2]
            str_content = line.split('_')[3].strip()
            regex_parameters = ''
            try:
                # Try to see if there is an additional field (the number of extracted parameters)
                regex_parameters = line.split('_')[4].strip()
            except IndexError:
                pass
            # When the intent name changes, create a new element in the dictionary of dictionaries
            if intent != prev_intent:
                prev_intent = intent
                common_ints[intent] = {}
            if str_type != prev_str_type:
                prev_str_type = str_type
                common_ints[intent][str_type] = []
            # If there are parameters it means that the string is a regex -> create a tuple element where the first
            # element is the regex, while the second is an array with the number of parameters
            if regex_parameters:
                # If there is only one parameter
                if len(regex_parameters) == 1:
                    regex_parameters = [int(regex_parameters)]
                    common_ints[intent][str_type].append((str_content, regex_parameters))
                # If there is more than one
                else:
                    regex_parameters = [int(param) for param in regex_parameters.split(",")]
                    common_ints[intent][str_type].append((str_content, regex_parameters))
            else:
                # Normal way to append regexes of the same intent
                common_ints[intent][str_type].append(str_content)

    # print(common_ints)
    return common_ints


# TODO: modify this function like the common one, but with topic numbers
# This function returns an array of dictionary of dictionary. Each element of the array corresponds to a topic, and
# to each topic is associated a dictionary containing all the intents with an associated dictionary containing the
# training phrases, the replies (if any), the kbplans (if any), and the plans (if any)
# [{'food0':{'t': [regexes], 'r': [replies], 'k': [kbplans], 'p': [plans]}, 'food1':{...}, ...}, {'music0':{...}, ..}]
def get_topics_intents():
    with open("dialogue_tree/topics_intents.txt", 'r') as f:
        lines = f.readlines()

    topics_ints = []
    prev_topic = -1
    prev_intent = ''
    prev_str_type = ''
    for line in lines:
        # If the line begins with an underscore, process the regex
        if line[0] == '_':
            topic = int(line.split('_')[1])
            intent = line.split('_')[2]
            str_type = line.split('_')[3]
            str_content = line.split('_')[4].strip()
            # When the topic number changes, create a new element in the array of dictionary of dictionaries
            if topic != prev_topic:
                prev_topic = topic
                topics_ints.append({})
            if intent != prev_intent:
                prev_intent = intent
                topics_ints[topic][intent] = {}
            if str_type != prev_str_type:
                prev_str_type = str_type
                topics_ints[topic][intent][str_type] = []
            topics_ints[topic][intent][str_type].append(str_content)

    return topics_ints


common_intents = get_common_intents()
# topics_intents = get_topics_intents()


# This function is essential because it's not possible to replace characters in a string overwriting it.
# In this way it returns a "copy" of the string with the replaced parameter and it works :-)
def replace(inp_str, i, what):
    replaced = inp_str.replace("$parameter" + str(i), what)
    return replaced


# This function takes a string (i.e., a reply, a kbplan or a plan) and replaces the parameters, if they are present
# in the dictionary of parameters of the matched trigger sentence of the corresponding intent
def replace_parameters(txt, regex_param_dict):
    # Suppose we don't have more that 10 parameters in a sentence
    for i in range(1, 10):
        if "$parameter" + str(i) in txt:
            print("\n$parameter" + str(i) + " found in " + txt)
            if "$parameter" + str(i) in regex_param_dict:
                print("$parameter" + str(i) + " is in the dictionary")
                txt = replace(txt, i, regex_param_dict["$parameter" + str(i)])
            # else:
            #    txt = replace(txt, i, "None")
    return txt


class RegexMatch(Resource):
    # If the other service performs a GET request
    def get(self, topic_n, sentence):
        print("Received sentence: ", sentence)
        reply = ''
        kbplan = ''
        plan = ''
        sentence = sentence.replace("_", " ")
        # Concatenate the intents of the topic with the common intents (putting before those of the topic)
        # considered_intents = {**topics_intents[topic_n], **common_intents}
        considered_intents = common_intents

        # Check if the sentence matches with a regex among those of all the common intents
        for intent in considered_intents:
            # Loop through the regexes of each intent to see if there is a match
            for trigger_sent in considered_intents[intent]['t']:
                regex = trigger_sent[0]
                params_number = trigger_sent[1]
                p = re.findall(regex, sentence)
                if p:
                    if isinstance(p[0], tuple):
                        p = p[0]
                    regex_param_dictionary = {}
                    print("Matched regex: ", regex)
                    for i in range(len(p)):
                        param_name = "$parameter" + str(params_number[i])
                        regex_param_dictionary[param_name] = p[i]
                    print(regex_param_dictionary)
                    # Choose a reply, a kbplan, a plan among those of the intent, if any, and replace the occurrences
                    # of $parameter#
                    if 'r' in common_intents[intent]:
                        reply = random.choice(considered_intents[intent]['r'])
                        reply = replace_parameters(reply, regex_param_dictionary)
                    if 'k' in common_intents[intent]:
                        kbplan = random.choice(considered_intents[intent]['k'])
                        kbplan = replace_parameters(kbplan, regex_param_dictionary)
                    if 'p' in common_intents[intent]:
                        plan = random.choice(considered_intents[intent]['p'])
                        plan = replace_parameters(plan, regex_param_dictionary)
                    break
        print(reply)
        return {"reply": reply, "plan": plan, "kbplan": kbplan}


api.add_resource(RegexMatch, "/regex_match/<int:topic_n>/<string:sentence>")


if __name__ == "__main__":
    # https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    # & openssl req - x509 - newkey rsa: 4096 - nodes - out cert.pem - keyout key.pem - days 365
    app.run(host="0.0.0.0", port=5001, debug=False)
    # ssl_context=('cert.pem', 'key.pem')
    # debug=True to make it restart when errors occur or changes are made
