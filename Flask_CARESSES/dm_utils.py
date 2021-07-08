import pickle
import random
import copy
from collections import defaultdict
from topics import choose_topic


# This function returns a dictionary where the key indicates when the sentence should be used during the dialogue,
# and the value is a list of all the alternative sentences of that type.
def retrieve_common_sentences():
    common_sent_dictionary = defaultdict(list)
    with open("dialogue_tree/common_sent.txt", 'r') as file:
        for row in file:
            if '_' in row:
                t = row.rstrip().split('_')[0]
                s = row.rstrip().split('_')[1]
                common_sent_dictionary[t].append(s)
    return common_sent_dictionary


common_sent_dict = retrieve_common_sentences()


# This function initializes the flags of all the topics sentences to zero.
def initialize_topics_sentences_flags(base_topics_sentences):
    base_topics_sentences_flags = []
    for i in range(len(base_topics_sentences)):
        base_topics_sentences_flags.append([])
        for sent in base_topics_sentences[i]:
            base_topics_sentences_flags[i].append(0)
    return base_topics_sentences_flags

# This function returns the topic used to start the conversation fort the first time, or every day, or
# in particular days (i.e., Christmas, Easter, etc.)
def get_starting_topics():
    init_topics = []
    with open("dialogue_tree/init_topics.txt", 'r') as f:
        for line in f:
            for topic in line.split():
                init_topics.append(int(topic))
    return init_topics


def choose_pattern(topic_n, topics_likeliness):
    with open("dialogue_tree/patterns.txt", 'rb') as file:
        patterns = pickle.load(file)

    print("Choosing pattern for topic ", topic_n)
    # If the likeliness is a value among 0 and 1 follow the pattern
    pattern = random.choice(patterns)

    # If the topic has likeliness 1 do not take questions into consideration
    if topics_likeliness[topic_n] == 1.0:
        print("Topic likeliness is 1. Delete questions from pattern.")
        pattern = [x for x in pattern if x != 'q']
    sentence_type = pattern[0]
    prev_topic_pattern = copy.deepcopy(pattern[1:])

    print("New pattern chosen!", sentence_type, prev_topic_pattern)
    return sentence_type, prev_topic_pattern


def choose_sentence(sentence_type, topic_sentences, topic_sentences_types, topic_sentences_flags, topic_likeliness):
    print("Choosing sentence of type: ", sentence_type)
    candidate_sentences = []
    no_sentences_of_that_type = True
    for t in range(len(topic_sentences_types)):
        # If the type of the sentence is the required one, and it has been not already said
        if topic_sentences_types[t] == sentence_type:
            no_sentences_of_that_type = False
            if topic_sentences_flags[t] == 0:
                candidate_sentences.append(topic_sentences[t])
    # If there are candidate sentences to be said, choose one randomly, and set its flag to 1
    if candidate_sentences:
        print("There are candidate sentences!")
        print(candidate_sentences, "cand sentences")
        chosen_sentence = random.choice(candidate_sentences)
        # If the sentence is a question...
        if sentence_type == 'q':
            # If the likeliness is not 0, once every 5 times add a common sentence of type q before the question
            if topic_likeliness != 0.0:
                if random.random() < 0.2:
                    chosen_sentence = random.choice(common_sent_dict['q']) + " " + chosen_sentence
            # If the likeliness is zero, add a common sentence of type 'z' before the sentence
            else:
                chosen_sentence = random.choice(common_sent_dict['z']) + " " + chosen_sentence
        # Flag the chosen sentence
        for s in range(len(topic_sentences)):
            if topic_sentences[s] == chosen_sentence:
                topic_sentences_flags[s] = 1
                print("Flagged chosen sentence.")
        print("Chosen sentence: ", chosen_sentence)
        return chosen_sentence
    else:
        if no_sentences_of_that_type:
            print("No sentences of this type")
            return ""
        else:
            print("No more candidate sentences! All flagged!")
            # Delete the flag from all the sentences of that type
            for t in range(len(topic_sentences_types)):
                # If the type of the sentence is the required one, and it has been not already said
                if topic_sentences_types[t] == sentence_type:
                    print("Unflag the sentence of type: ", sentence_type)
                    topic_sentences_flags[t] = 0
            # Call the function again with the all the flags set to zero
            return choose_sentence(sentence_type, topic_sentences, topic_sentences_types, topic_sentences_flags,
                                   topic_likeliness)


def explore_DT(response, prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
               topics_children, topics_brothers, topics_likeliness,
               topics_sentences, topics_sentences_types, topics_sentences_flags, negative):
    # If the pattern is not finished, continue
    if prev_topic_pattern:
        print("Previous topic still has a pattern: ", prev_topic_pattern)
        sentence_type = prev_topic_pattern[0]
        try:
            prev_topic_pattern = prev_topic_pattern[1:]
        except:
            prev_topic_pattern = []
        print("Next sentence type: ", sentence_type)
        print("Next sentences type (updated): ", prev_topic_pattern)
        resp = choose_sentence(sentence_type, topics_sentences[prev_topic_number],
                               topics_sentences_types[prev_topic_number], topics_sentences_flags[prev_topic_number],
                               topics_likeliness[prev_topic_number])
        response = response + " " + resp
        print("Concatenated responses: ", response)

        if resp == "":
            print("No response available, continue.")
            prev_topic_pattern = prev_topic_pattern[1:]
            return explore_DT(response, prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
                              topics_children, topics_brothers, topics_likeliness, topics_sentences,
                              topics_sentences_types, topics_sentences_flags, False)
        topic_n = prev_topic_number
    # If the pattern is finished, choose among children - descend the tree
    else:
        print("EMPTY PATTERN")
        if negative:
            if prev_topic_stop:
                # Do not allow to choose father's brothers with likeliness zero
                # topic_n = choose_topic(topics_brothers[topics_father[prev_topic_number]], topics_likeliness, False)
                # Do not jump further - end conversation
                topic_n = -1
                prev_topic_stop = False
                # print("Second NEGATIVE answer: CHOOSE NEW TOPIC AMONG FATHER's BROTHERS")
                print("Second NEGATIVE answer: END CONVERSATION")
            else:
                # Do not allow to choose brothers with likeliness zero
                topic_n = choose_topic(topics_brothers[prev_topic_number], topics_likeliness, False)
                prev_topic_stop = True
                print("NEGATIVE answer: CHOOSE NEW TOPIC AMONG BROTHERS")
        else:
            # Do not allow to choose children with likeliness zero
            topic_n = choose_topic(topics_children[prev_topic_number], topics_likeliness, False)
            print("Descend the DT: CHOOSE NEW TOPIC AMONG CHILDREN")

        # If there are children/brothers with likeliness != 0, jump to one of them
        if topic_n != -1:
            prev_topic_number = topic_n
            sentence_type, prev_topic_pattern = choose_pattern(topic_n, topics_likeliness)
            resp = choose_sentence(sentence_type, topics_sentences[topic_n],
                                   topics_sentences_types[topic_n], topics_sentences_flags[topic_n],
                                   topics_likeliness[topic_n])
            response = response + " " + resp
        # If there are no children/brothers or no children/brothers with likeliness != 0, end.
        else:
            topic_n = prev_topic_number
            print("No children/brothers/father's brothers (or none with non zero likeliness")
            sentence_type = 'e'
            prev_topic_pattern = []
            response = response + " " + random.choice(common_sent_dict['e'])
    # If the sentence is positive, call this function again
    if sentence_type == 'p':
        # prev_topic_pattern = prev_topic_pattern[1:]
        print("POSITIVE sentence, update the pattern to: ", prev_topic_pattern)
        return explore_DT(response, prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
                          topics_children, topics_brothers, topics_likeliness, topics_sentences, topics_sentences_types,
                          topics_sentences_flags, False)
    if sentence_type == 'n':
        print("NEGATIVE sentence")
        return explore_DT(response, prev_topic_number, prev_topic_pattern, prev_topic_stop, topics_father,
                          topics_children, topics_brothers, topics_likeliness, topics_sentences, topics_sentences_types,
                          topics_sentences_flags, True)

    return sentence_type, prev_topic_pattern, response, topic_n, prev_topic_stop


def start_new_pattern(topic_n, prev_topic_stop, topics_father, topics_children,
                      topics_brothers, topics_likeliness, topics_sentences, topics_sentences_types,
                      topics_sentences_flags):
    sentence_type, prev_topic_pattern = choose_pattern(topic_n, topics_likeliness)
    print("Chosen pattern of new topic: ", sentence_type, prev_topic_pattern)
    response = choose_sentence(sentence_type, topics_sentences[topic_n],
                               topics_sentences_types[topic_n], topics_sentences_flags[topic_n],
                               topics_likeliness[topic_n])
    while response == "" or sentence_type == 'p':
        sentence_type, prev_topic_pattern, response, topic_n, prev_topic_stop = \
            explore_DT("", topic_n, prev_topic_pattern, prev_topic_stop, topics_father, topics_children,
                       topics_brothers, topics_likeliness, topics_sentences, topics_sentences_types,
                       topics_sentences_flags, False)

    return sentence_type, prev_topic_pattern, response, topic_n, prev_topic_stop


# This function updates all the files of the client, before returning the response.
def update_files(client_id, topics_sentences_flags, topics_likeliness, topic_counter):
    # Update sentences flags
    with open('clients/' + str(client_id) + "/sentences_flags.txt", 'wb') as file:
        pickle.dump(topics_sentences_flags, file)

    # Update likelinesses
    with open('clients/' + str(client_id) + "/likelinesses.txt", 'wb') as file:
        pickle.dump(topics_likeliness, file)

    # Update topic counter
    with open('clients/' + str(client_id) + "/topic_counter.txt", 'wb') as file:
        pickle.dump(topic_counter, file)
