from flask import Flask
from flask_restful import Api, Resource
from topics import *
from topics_utils import *
from client_utils import *
from dm_utils import *
import datetime
import requests
import re

# TODO: fix jumping to topic with same keywords but wrong likeliness (e.g., music -> 800, 1440)
# TODO: return separately intent reply plan and reply

app = Flask(__name__)
api = Api(app)

# IP of where the service for regex match is running
regex_ip = "127.0.0.1"
# Port for the request to the regex match service
regex_port = 5001

print("Starting dialogue manager. Please wait some seconds...")

# ------ RETRIEVE BASIC STUFF FROM FILES GENERATED STARTING FROM THE ONTOLOGY ------
# Get topic names, likelinesses and keywords (from triggering_keyword.json) - CHECKED
base_id_reqs, _, base_req_par1, base_req_par2, base_tot_topic = get_topics_keywords_and_likelinesses()

# Get the relationships between topics - father, children, brothers, and likeliness - CHECKED
base_top_topics, base_topics_father, base_topics_children, base_topics_brothers, base_topics_likeliness = \
    get_topics_relationships()

# Get the topics, the types of the sentences, the sentences (from sentences.enu files) - CHECKED
base_topics_sentences_types, base_topics_sentences = get_topics_sentences()

# Initialize the flags of all topics sentences to zero
base_topics_sentences_flags = initialize_topics_sentences_flags(base_topics_sentences)

# To get school subject topic number
schoolsubjects_topic_numbers = get_school_topic()
print(schoolsubjects_topic_numbers)

# ---------- RETRIEVE CLIENTS DATA ---------
# Get topic names, likelinesses and keywords associated to each client ID - CHECKED
clients_id_reqs, clients_req_par1, clients_req_par2, clients_tot_topic = \
    get_clients_topics_keywords_and_likelinesses(base_id_reqs, base_req_par1, base_req_par2, base_tot_topic)

# Get the relationships between topics for all clients - CHECKED
clients_top_topics, clients_topics_father, clients_topics_children, clients_topics_brothers = \
    get_clients_topics_relationships(base_top_topics, base_topics_father, base_topics_children, base_topics_brothers)

# Get the clients types of sentences and the sentences - CHECKED
clients_topics_sentences_types, clients_topics_sentences = \
    get_clients_topics_sentences(base_topics_sentences_types, base_topics_sentences)
#print(clients_topics_sentences, "print")

# Get likelinesses from other file
clients_topics_likeliness = get_clients_topics_likeliness()

# Get the topic counter of the already existing client IDs - CHECKED
clients_topic_counter = get_clients_topic_counter()

# Get the already said sentences for the existing client IDs - CHECKED
clients_topics_sentences_flags = get_clients_topics_sentences_flags()


# The dictionary contains as keys the types of the sentences (where they should be used), and as values the sentences
common_sent_dict = retrieve_common_sentences()

current_id = len(clients_topic_counter)

init_topics = get_starting_topics()

#print(clients_topic_counter[0])

def procedure(client_id, sentence, intent_reply):
    # Store all needed parameters
    id_reqs = clients_id_reqs[client_id]
    req_par1 = clients_req_par1[client_id]
    req_par2 = clients_req_par2[client_id]
    tot_topic = clients_tot_topic[client_id]

    topic_counter = clients_topic_counter[client_id]
    prev_topic_number = topic_counter[0]
    prev_topic_sentence_type = topic_counter[1]
    prev_topic_pattern = topic_counter[2]
    prev_topic_stop = topic_counter[3]
    prev_topic_time = topic_counter[4]

    topics_father = clients_topics_father[client_id]
    topics_brothers = clients_topics_brothers[client_id]
    topics_children = clients_topics_children[client_id]

    topics_sentences = clients_topics_sentences[client_id]
    topics_sentences_types = clients_topics_sentences_types[client_id]
    topics_sentences_flags = clients_topics_sentences_flags[client_id]

    topics_likeliness = clients_topics_likeliness[client_id]


    # TODO: maybe it's better to put these answers in a file and use a broader set - maybe use a regex?
    pos_user_answers = ["yes", "Yes", "ok", "Ok", "Fine", "sure", "Sure", "Of course", "of course"]
    neg_user_answers = ["No", "no"]

    perform_goal = 0
    show_interest = False
    school_topic = schoolsubjects_topic_numbers
    print(school_topic)
    # Check the type of the previous sentence:
    if prev_topic_sentence_type == 'q':
        print("Expecting answer to a question")
        sentiment = 0
        # If the answer contains yes, change the likeliness of the previous topic to 1

        if any(word in sentence for word in pos_user_answers):
            sentiment = 1
            if prev_topic_number not in school_topic:
                topics_likeliness[prev_topic_number] = 1.0
                print("Setting likeliness of topic ", prev_topic_number, " to 1.0")
        elif any(word in sentence for word in neg_user_answers):
            sentiment = -1
            if prev_topic_number not in school_topic:
                topics_likeliness[prev_topic_number] = 0.0
                print("Setting likeliness of topic ", prev_topic_number, " to 0.0")

        # Check if the sentence is related to a topic
        # Allow topics with likeliness zero
        topic_n = main(sentence, id_reqs, topics_likeliness, req_par1, req_par2, tot_topic)
        # If a topic associated to the sentence is found
        if topic_n != -1:
            # If the topic is the same as the previous one
            if topic_n == prev_topic_number:
                # If the answer is not negative, try to continue with the same topic
                if sentiment != -1:
                    # Insert a positive sentence as next element of the pattern
                    prev_topic_pattern.insert(0, 'p')
                    print("Added positive sentence type to answer to the positive answer")
                    negative = False

                    if prev_topic_number in school_topics:
                        for number_of_questions in range(2):
                            question = choose_sentence('p', topics_sentences[prev_topic_number],
                                                       topics_sentences_types[prev_topic_number],
                                                       topics_sentences_flags[prev_topic_number],
                                                       topics_likeliness[prev_topic_number])

                # If the sentiment is negative
                else:
                    prev_topic_pattern = ['n']
                    print("Added negative sentence type to answer to the negative answer")
                    negative = True


                sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                    explore_DT("", prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
                               topics_children, topics_brothers, topics_likeliness, topics_sentences,
                               topics_sentences_types, topics_sentences_flags, negative)
            # If the triggered topic is not the same as the previous one, jump to that
            else:
                # Choose a new pattern
                print("Jumping to topic: ", topic_n)
                print("Topic likeliness: ", topics_likeliness[topic_n])
                # Start a new pattern for the new topic
                sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                    start_new_pattern(topic_n, prev_topic_stop, topics_father, topics_children, topics_brothers,
                                      topics_likeliness, topics_sentences, topics_sentences_types,
                                      topics_sentences_flags)
                # Check if the likeliness of the returned topic is zero -> ask confirmation!
                if topics_likeliness[topic_n] == 0:
                    reply = "I thought you didn't like it..." + reply

        # If no topic associated to the sentence is found
        else:
            print("No topic associated to sentence found.")
            if sentiment != -1:
                print("Prev topic number: ", prev_topic_number)
                prev_topic_pattern.insert(0, 'p')
                print("Added positive sentence type to pattern to answer to user's sentence")

                negative = False
            # If no topic is found and the user said no, go to negative
            else:
                negative = True
                prev_topic_pattern = ['n']
                print("Added negative sentence type to pattern to answer to user's sentence")
            sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                explore_DT("", prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
                           topics_children, topics_brothers, topics_likeliness, topics_sentences,
                           topics_sentences_types, topics_sentences_flags, negative)
    #elif prev_topic_sentence_type == 'p':
    #    sentiment = 0
    #    #for i in range
    #    if prev_topic_number in school_topic:
    #        current_school_topic = prev_topic_number

    #        for school_sentences in base_topics_sentences:
    #            index = 1
    #            question = ("_" + str(index) + "q")
    #            answer = ("_" + str(index) + "a")
    #            if question in school_sentences:
    #                print(school_sentences)
    #                if any(word in sentence for word in pos_user_answers):
    #                    sentiment = 1
    #                if any(word in sentence for word in neg_user_answers):
    #                    sentiment = -1
                    # If the answer is not negative, try to continue with the same topic
    #                    if sentiment != -1:
    #                        if answer in school_sentences:
    #                            print(school_sentences, "Would you like to know more")
                        # If the sentiment is negative
    #                        else:
    #                            break

    #        question = choose_sentence('q', topics_sentences[prev_topic_number] , topics_sentences_types[prev_topic_number], topics_sentences_flags[prev_topic_number], topics_likeliness[prev_topic_number])
    #elif prev_topic_sentence_type == 'p':
    #    print("Posv Sent")
    #    if prev_topic_number in school_topics:
    #        #if
    #        for number_of_questions in range(2):
    #            question = choose_sentence('q', topics_sentences[prev_topic_number] , topics_sentences_types[prev_topic_number], topics_sentences_flags[prev_topic_number], topics_likeliness[prev_topic_number])

    # If we are at the end
    elif prev_topic_sentence_type == 'e':
        print("---------- REACHED END STATE ----------")
        # Check if the user's sentence contains keywords
        # Allow also topics with likeliness zero, if no other topics are found
        topic_n = main(sentence, id_reqs, topics_likeliness, req_par1, req_par2, tot_topic)
        common_sent = ''
        # If no topic is triggered by the user's sentence, choose it from top concepts
        if topic_n == -1:
            print("No topic triggered by the user: choose from top concepts")
            topic_n = choose_topic(clients_top_topics[client_id], topics_likeliness, False)
            # The sentence to be added at the beginning will be one of those to be put before a top concept
            common_sent = random.choice(common_sent_dict['r'])
        # Start a new pattern for the new topic
        sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
            start_new_pattern(topic_n, prev_topic_stop, topics_father, topics_children, topics_brothers,
                              topics_likeliness, topics_sentences, topics_sentences_types, topics_sentences_flags)
        # If there is a topic associated with the sentence (hence the common sentence has not been assigned yet)
        if not common_sent:
            # Check if the likeliness of the topic is zero: add a "check" sentence before making the question:
            common_sent = "I thought you didn't like it..."
            # If the topic doesn't have likeliness 0 or 1, add a common sentence among those to be said before questions
            if 0.0 < float(topics_likeliness[topic_n]) < 1.0:
                common_sent = random.choice(common_sent_dict['q'])
            # If the topic has likeliness 1 it will say a positive or a wait depending on the pattern, without adding
            # nothing before.

        reply = common_sent + " " + reply

    # If sentence type w, c, g
    else:
        if prev_topic_sentence_type == 'g':
            if any(word in sentence for word in pos_user_answers):
                perform_goal = 1
            elif any(word in sentence for word in neg_user_answers):
                perform_goal = -1
        else:
            # Show interest only if it's the answer to a wait during the dialogue.
            # If it's a wait as a response to an intent that set the likeliness to 1 do not show too much interest!
            if not intent_reply:
                print("SHOW INTEREST AFTER A WAIT!")
                show_interest = True

        # Check if the user's sentence is related to a topic - allow also topics with likeliness 0
        topic_n = main(sentence, id_reqs, topics_likeliness, req_par1, req_par2, tot_topic)
        # If a topic associated to the sentence is found
        if topic_n != -1:
            # If the topic is the same as the previous one
            if topic_n == prev_topic_number:
                # Try to continue with the same topic or choose a son, or end.
                sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                    explore_DT("", topic_n, prev_topic_pattern, prev_topic_stop, topics_father,
                               topics_children, topics_brothers, topics_likeliness, topics_sentences,
                               topics_sentences_types, topics_sentences_flags, False)

            # If the triggered topic is not the same as the previous one, jump to that
            else:
                # Start a new pattern for the new topic
                sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                    start_new_pattern(topic_n, prev_topic_stop, topics_father, topics_children, topics_brothers,
                                      topics_likeliness, topics_sentences, topics_sentences_types,
                                      topics_sentences_flags)
                # If the likeliness of the topic is 0, add a "doubt" sentence before
                if topics_likeliness[topic_n] == 0.0:
                    # TODO: put these sentences in the common_sent file and choose randomly every time
                    reply = "I thought you didn't like it..." + reply

        # If no topic associated to the user's sentence is found
        else:
            print("No topic associated to the sentence found: try to continue")
            sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                explore_DT("", prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
                           topics_children, topics_brothers, topics_likeliness, topics_sentences,
                           topics_sentences_types, topics_sentences_flags, False)
        if perform_goal == 1:
            # Or choose between gp sentences in case the goal could be accomplished
            reply = "Sorry, I can't do that. " + reply
        elif perform_goal == -1:
            reply = random.choice(common_sent_dict['gn']) + " " + reply
        elif show_interest:
            reply = random.choice(common_sent_dict['w']) + " " + reply

    return sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop


class FindTopic(Resource):
    # If the client performs a GET request, it means that the ID already exists.
    def get(self, client_id, sentence):
        # Save all data related to the current client
        client_id = int(client_id)
        id_reqs = clients_id_reqs[client_id]
        req_par1 = clients_req_par1[client_id]
        req_par2 = clients_req_par2[client_id]
        tot_topic = clients_tot_topic[client_id]

        topic_counter = clients_topic_counter[client_id]
        prev_topic_number = topic_counter[0]
        prev_topic_sentence_type = topic_counter[1]
        prev_topic_pattern = topic_counter[2]
        prev_topic_stop = topic_counter[3]
        prev_topic_time = topic_counter[4]

        topics_father = clients_topics_father[client_id]
        topics_brothers = clients_topics_brothers[client_id]
        topics_children = clients_topics_children[client_id]

        topics_sentences = clients_topics_sentences[client_id]
        topics_sentences_types = clients_topics_sentences_types[client_id]
        topics_sentences_flags = clients_topics_sentences_flags[client_id]

        topics_likeliness = clients_topics_likeliness[client_id]

        print("\n-----------------------------------------------")
        print("CLIENT: ", client_id)
        print("STATE: ", topic_counter)

        do_procedure = True
        topic_n = prev_topic_number
        sentence_type = prev_topic_sentence_type
        reply = ''

        # TODO: if there is no topic match with a certain regex, try with other regex
        # ---------- Call the service for matching patterns ----------
        print("\n ---------- CALLING REGEX MATCH SERVICE ----------")
        try:
            response = requests.get("http://" + regex_ip + ":" + str(regex_port) + "/regex_match/" + str(prev_topic_number)
                                    + "/" + sentence, verify=False)
            print(response.json())
            intent_reply = response.json()['reply']
            kbplan = response.json()['kbplan']
            plan = response.json()['plan']
        except requests.exceptions.ConnectionError as e:
            print(e)
            intent_reply = ''
            kbplan = ''
            plan = ''

        # If a topic is found in the regex it will be replaced, and it will be passed as parameter to the procedure
        topic = sentence
        if kbplan:
            kbplan_items = kbplan.split('#')[1:]
            print(kbplan_items)
            for item in kbplan_items:
                # The action is supposed to be made of 1 word
                action = re.findall("action=(\w+)", item)[0]
                # The topic extracted could be of more than a word
                topic = re.findall("topic=(.*) (?:startsentence|value)", item)[0]
                print(topic)
                if topic:
                    # Add spaces before and after the topic to have keyword match when it's just one word
                    topic = " " + topic + " "
                    # Setting the last parameter to true allows to return topics with zero likeliness (if no others)
                    topic_n = main(topic, id_reqs, topics_likeliness, req_par1, req_par2, tot_topic)
                else:
                    topic_n = -1
                if action == 'setlikeliness':
                    print("---- SETLIKELINESS action ----")
                    if topic_n != -1:
                        likeliness = re.findall("value=(\d+.\d+)", item)[0]
                        likeliness = float(likeliness)
                        if 0.0 < likeliness < 1.0:
                            likeliness = max(float(topics_likeliness[topic_n]), likeliness)
                        print("Setting likeliness of topic", topic_n, "to", str(likeliness))
                        topics_likeliness[topic_n] = likeliness
                if action == 'jump':
                    print("---- JUMP action ----")
                    startsentence = re.findall("startsentence=(\w+)", item)[0]
                    if startsentence == 'n':
                        do_procedure = False
                        # Set prev topic stop to false as it is not considered as saying "no" for the second time to a
                        # question. In this way it jumps to a brother if you say "I hate/I don't want to talk about"
                        prev_topic_stop = False
                        prev_topic_pattern = []
                        sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                            explore_DT("", topic_n, prev_topic_pattern, prev_topic_stop, topics_father,
                                       topics_children, topics_brothers, topics_likeliness,
                                       topics_sentences, topics_sentences_types, topics_sentences_flags, True)

        # TODO: check if the parameters are changed in the correct way
        if do_procedure:
            # NB: the procedure is called passing the topic extracted as parameter and not the full sentence
            sentence_type, prev_topic_pattern, reply, topic_n, prev_topic_stop = \
                procedure(client_id, topic, intent_reply)

        time = datetime.datetime.now()

        print("Update sentence type to: ", sentence_type)
        print("Update next sentences types to: ", prev_topic_pattern)
        print("Updating topic counter with topic: ", topic_n)
        clients_topic_counter[client_id] = [topic_n, sentence_type, prev_topic_pattern, prev_topic_stop, time]

        update_files(client_id, topics_sentences_flags, topics_likeliness, topic_counter)

        # Delete eventual spaces at the beginning and at the end of the reply
        reply = reply.strip()
        # TODO: check why there is no plan returned
        print("The plan is", plan)
        return {"topic": topic_n, "intent_reply": intent_reply, "plan": plan, "reply": reply}

    # This function manages the put request which is the request made by the client the first time it connects to the
    # dialogue management service.
    def put(self, client_id, sentence):
        global current_id
        global init_topics
        absolute_start_topic = init_topics[0]

        client_id = current_id
        current_id = current_id + 1
        path = os.path.join("clients", str(client_id))
        os.mkdir(path)

        open('clients/' + str(client_id) + "/triggering_keyword.json", 'w')
        clients_id_reqs.append(base_id_reqs)
        clients_req_par1.append(base_req_par1)
        clients_req_par2.append(base_req_par1)
        clients_tot_topic.append(base_tot_topic)

        open('clients/' + str(client_id) + "/resume.csv", 'w')
        clients_top_topics.append(base_top_topics)
        clients_topics_father.append(base_topics_father)
        clients_topics_children.append(base_topics_children)
        clients_topics_brothers.append(base_topics_brothers)

        open('clients/' + str(client_id) + "/sentences.enu", 'w')
        clients_topics_sentences_types.append(base_topics_sentences_types)
        clients_topics_sentences.append(base_topics_sentences)

        with open('clients/' + str(client_id) + "/likelinesses.txt", 'wb') as f:
            pickle.dump(base_topics_likeliness, f)
        clients_topics_likeliness.append(base_topics_likeliness)

        sentence_type, prev_topic_pattern = choose_pattern(absolute_start_topic, clients_topics_likeliness[client_id])

        with open('clients/' + str(client_id) + "/topic_counter.txt", 'wb') as f:
            time = datetime.datetime.now()
            pickle.dump([absolute_start_topic, sentence_type, prev_topic_pattern, False, time], f)
        clients_topic_counter.append([init_topics[0], sentence_type, prev_topic_pattern, False, time])

        with open('clients/' + str(client_id) + "/sentences_flags.txt", 'wb') as f:
            pickle.dump(base_topics_sentences_flags[client_id], f)
        clients_topics_sentences_flags.append(base_topics_sentences_flags)

        reply = choose_sentence(sentence_type, clients_topics_sentences[client_id][absolute_start_topic],
                                clients_topics_sentences_types[client_id][absolute_start_topic],
                                clients_topics_sentences_flags[client_id][absolute_start_topic],
                                clients_topics_likeliness[client_id][absolute_start_topic])

        return {"id": client_id, "reply": reply}


api.add_resource(FindTopic, "/caresses/<string:client_id>/<string:sentence>")

if __name__ == "__main__":
    # https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    # & openssl req - x509 - newkey rsa: 4096 - nodes - out cert.pem - keyout key.pem - days 365
    app.run(host="0.0.0.0", debug=False)
    # Default running on port 5000
    # ssl_context=('cert.pem', 'key.pem')
    # debug=True to make it restart when errors occur or changes are made
