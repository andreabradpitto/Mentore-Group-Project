"""
Author:      Lucrezia Grassi
Email:       lucrezia.grassi@edu.unige.it
Affiliation: Laboratorium, DIBRIS, University of Genoa, Italy
Project:     CARESSES (http://caressesrobot.org/en/)

This file contains all the functions needed to retrieve clients data before starting the dialogue management service
"""

import os
import csv
import json
import pickle
import copy


# Function that returns the types of the sentences and the sentences
def get_clients_topics_sentences(base_topics_sentences_types, base_topics_sentences):
    clients_topics_sentences_types = []
    clients_topics_sentences = []

    topics_sentences_types = copy.deepcopy(base_topics_sentences_types)
    topics_sentences = copy.deepcopy(base_topics_sentences)

    for folder in os.listdir("clients"):
        if os.stat("clients/" + str(folder) + "/sentences.enu").st_size != 0:
            # Consider as current topic the last already existing topic
            curr_topic = len(base_topics_sentences_types) - 1
            with open("clients/" + str(folder) + "/sentences.enu") as file:
                lines = file.readlines()
                if lines:
                    for line in lines:
                        if line[0] == '_':
                            sentence_type = line.split('#')[1].split('\n')[0]
                            if sentence_type[0] == 'g':
                                sentence_type = sentence_type.split('&')[0]
                            tmp = line.replace(':', '_')
                            tmp = tmp.replace('#', '_')
                            split = tmp.split('_')
                            topic_num = int(split[1])
                            sentence = split[3]

                            # Delete spaces at the beginning and end of the sentence
                            if sentence[0] == ' ':
                                sentence = sentence[1:]
                            if sentence[-1] == ' ':
                                sentence = sentence[:-1]

                            # If the topic is still the same, fill the sen
                            if topic_num == curr_topic:
                                topics_sentences_types[topic_num].append(sentence_type)
                                topics_sentences[topic_num].append(sentence)

                            else:
                                curr_topic = topic_num
                                topics_sentences_types.append([sentence_type])
                                topics_sentences.append([sentence])

        clients_topics_sentences_types.append(topics_sentences_types)
        clients_topics_sentences.append(topics_sentences)

    return clients_topics_sentences_types, clients_topics_sentences


# Returns the keywords and the likelinesses of all clients - if no new
def get_clients_topics_keywords_and_likelinesses(base_id_reqs,
                                                 base_req_par1, base_req_par2, base_tot_topic):
    clients_id_reqs = []
    clients_req_par1 = []
    clients_req_par2 = []
    clients_tot_topic = []
    for folder in os.listdir("clients"):
        # Initialize arrays containing the fields of the json
        id_reqs = copy.deepcopy(base_id_reqs)
        req_par1 = copy.deepcopy(base_req_par1)
        req_par2 = copy.deepcopy(base_req_par2)
        tot_topic = copy.deepcopy(base_tot_topic)
        if os.stat("clients/" + str(folder) + "/triggering_keyword.json").st_size != 0:
            with open("clients/" + str(folder) + "/triggering_keyword.json", 'r') as json_file:
                data = json.load(json_file)
                for talk in data.values():
                    id_reqs.append(talk.get('id_request').split("#")[0])
                    req_par1.append(talk.get('request_parameters_1'))
                    req_par2.append(talk.get('request_parameters_2'))
                    tot_topic = tot_topic + 1

        clients_id_reqs.append(id_reqs)
        clients_req_par1.append(req_par1)
        clients_req_par2.append(req_par2)
        clients_tot_topic.append(tot_topic)

    return clients_id_reqs, clients_req_par1, clients_req_par2, clients_tot_topic


# This function returns the father, the children, the brothers and the likeliness of each topic
def get_clients_topics_relationships(base_top_topics, base_topics_father, base_topics_children,
                                     base_topics_brothers):
    start_topic = len(base_topics_father)
    clients_top_topics = []
    clients_topics_father = []
    clients_topics_children = []
    clients_topics_brothers = []
    for folder in os.listdir("clients"):
        top_topics = copy.deepcopy(base_top_topics)
        topics_father = copy.deepcopy(base_topics_father)
        topics_children = copy.deepcopy(base_topics_children)
        topics_brothers = copy.deepcopy(base_topics_brothers)
        if os.stat("clients/" + str(folder) + "/resume.csv").st_size != 0:
            with open("clients/" + str(folder) + "/resume.csv", 'r') as csv_file:
                max_topic = 0
                for r in csv.reader(csv_file):
                    # Add the father of new topics
                    topics_father.append(int(r[2]))
                    if int(r[1]) > max_topic:
                        max_topic = int(r[1])

            for topic in range(start_topic, max_topic + 1):
                father = topics_father[topic]
                # Add the topic as child of the already existing father
                topics_children[father].append(topic)

                # Prepare empty elements for new topic's children and brothers
                topics_children.append([])
                topics_brothers.append([])

                # For all the topics that have the same father, add the topic as brother
                for t in topics_children[father]:
                    # If the son is the new topic, add all the other children as brothers
                    if t != topic:
                        topics_brothers[t].append(topic)
                        topics_brothers[topic].append(t)

                if topic == father:
                    top_topics.append(topic)
                    top_concept = True
                else:
                    top_concept = False

                with open("clients/" + str(folder) + "/resume.csv", 'r') as csv_in:
                    for r in csv.reader(csv_in):
                        candidate = int(r[1])
                        candidate_father = int(r[2])
                        # If the candidate brother is not the topic I'm considering...
                        if candidate != topic:
                            # If the topic I'm considering is a top concept, all the top concepts are its brothers
                            if top_concept:
                                if candidate == candidate_father and topic < start_topic:
                                    topics_brothers[topic].append(candidate)
                            # If the topic is not a top concept, its brothers are those with the same father
                            # that are not top concepts!
                            else:
                                if candidate_father == father and candidate != candidate_father and topic < start_topic:
                                    topics_brothers[topic].append(candidate)
                            if candidate_father == topic and topic < start_topic:
                                topics_children[topic].append(candidate)

        clients_top_topics.append(top_topics)
        clients_topics_father.append(topics_father)
        clients_topics_children.append(topics_children)
        clients_topics_brothers.append(topics_brothers)

    return clients_top_topics, clients_topics_father, clients_topics_children, clients_topics_brothers


# This function returns an array containing the topic counter of all clients.
# The topic counter contains the topic, the sentence type, and a boolean variable to indicate
# whether two negative answers have been given)
def get_clients_topic_counter():
    clients_topic_counter = []
    for folder in os.listdir("clients"):
        topic_counter = []
        if os.stat("clients/" + str(folder) + "/topic_counter.txt").st_size != 0:
            with open("clients/" + str(folder) + "/topic_counter.txt", 'rb') as file:
                topic_counter = pickle.load(file)
        clients_topic_counter.append(topic_counter)
    return clients_topic_counter


# This function gets the likelinesses of the topics for all clients
def get_clients_topics_likeliness():
    clients_topics_likeliness = []
    for folder in os.listdir("clients"):
        topics_likeliness = []
        if os.stat("clients/" + str(folder) + "/likelinesses.txt").st_size != 0:
            with open("clients/" + str(folder) + "/likelinesses.txt", 'rb') as file:
                topics_likeliness = pickle.load(file)
        clients_topics_likeliness.append(topics_likeliness)
    return clients_topics_likeliness


# This function returns an array with the flags of the already said sentences
def get_clients_topics_sentences_flags():
    clients_sentences_flags = []
    for folder in os.listdir("clients"):
        if os.stat("clients/" + str(folder) + "/sentences_flags.txt").st_size != 0:
            with open("clients/" + str(folder) + "/sentences_flags.txt", 'rb') as file:
                clients_sentences_flags.append(pickle.load(file))
    return clients_sentences_flags

