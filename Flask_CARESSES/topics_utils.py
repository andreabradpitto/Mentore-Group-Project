"""
Author:      Lucrezia Grassi
Email:       lucrezia.grassi@edu.unige.it
Affiliation: Laboratorium, DIBRIS, University of Genoa, Italy
Project:     CARESSES (http://caressesrobot.org/en/)

This file contains all the functions needed to retrieve topics data before starting the dialogue management service
"""

import csv
import json

# Function that returns three arrays containing the topic numbers, the types of the sentences and the sentences
def get_topics_sentences():
    curr_topic = 0
    topics_sentences_types = [[]]
    topics_sentences = [[]]
    file = open("dialogue_tree/sentences.enu", 'r')
    lines = file.readlines()

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
    return topics_sentences_types, topics_sentences


def get_topics_keywords_and_likelinesses():
    # Open the json file containing the keywords
    with open('dialogue_tree/triggering_keyword.json') as f:
        data = json.load(f)

    # Initialize arrays containing the fields of the json
    id_reqs = []
    topics_likeliness = []
    req_par1 = []
    req_par2 = []
    tot_topic = -1
    for talk in data.values():
        id_reqs.append(talk.get('id_request').split("#")[0])
        topics_likeliness.append(talk.get('id_request').split("#")[1])
        req_par1.append(talk.get('request_parameters_1'))
        req_par2.append(talk.get('request_parameters_2'))
        tot_topic = tot_topic + 1
    print(tot_topic)
    return id_reqs, topics_likeliness, req_par1, req_par2, tot_topic


# This function returns the father, the children, the brothers and the likeliness of each topic
def get_topics_relationships():
    topics_likeliness = []
    topics_father = []
    top_topics = []
    with open('dialogue_tree/resume.csv', 'r') as csv_file:
        max_topic = 0
        for r in csv.reader(csv_file):
            topics_likeliness.append(r[3])  #what is r
            topics_father.append(int(r[2]))
            if int(r[1]) > max_topic:
                max_topic = int(r[1])

    topics_children = []
    topics_brothers = []
    # For each topic look for its brothers
    for topic in range(max_topic + 1):
        #print(topic)
        father = topics_father[topic]
        if topic == father:
            top_topics.append(topic)
            top_concept = True
        else:
            top_concept = False

        topics_children.append([])
        topics_brothers.append([])
        with open('dialogue_tree/resume.csv', 'r') as csv_in:
            for r in csv.reader(csv_in):
                candidate = int(r[1])
                candidate_father = int(r[2])
                # If the candidate brother is not the topic I'm considering...
                if candidate != topic:
                    # If the topic I'm considering is a top concept, all the top concepts are its brothers
                    if top_concept:
                        if candidate == candidate_father:
                            topics_brothers[topic].append(candidate)
                    # If the topic is not a top concept, its brothers are those with the same father
                    else:
                        if candidate_father == father and candidate != candidate_father:
                            topics_brothers[topic].append(candidate)
                    if candidate_father == topic:
                        topics_children[topic].append(candidate)
    #print(top_topics)
    return top_topics, topics_father, topics_children, topics_brothers, topics_likeliness

def get_school_topic():
    topics_likeliness = []
    topics_father = []
    topic_numbers_schoolsubjects = []
    topic_name = []
    school_topics = []
    topic_numbers = []

    with open('dialogue_tree/resume.csv', 'r') as csv_file:
        max_topic = 0
        for r in csv.reader(csv_file):
            topic_name.append(r[0])
            topics_likeliness.append(r[3])
            topics_father.append(int(r[2]))
            topic_numbers.append(int(r[1]))

        #for topic_name_schoolsubject in topic_name:
        for i, topic_name_schoolsubject in enumerate(topic_name):
                if topic_name_schoolsubject == "SCHOOLSUBJECT":
                    school_father = topics_father[i]
                    print(school_father)
                if topics_father[i] == school_father:
                    #print(topic_name_schoolsubject)
                    topic_numbers_schoolsubjects.append(topic_numbers[i])
        #print(topic_numbers_schoolsubjects)
    return topic_numbers_schoolsubjects
get_school_topic()