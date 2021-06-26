# Carmine: here a python script with some methods for modifying the Ontology:
# in particular, give a look to add_class_to_ontology and add_individual_to_ontology

# This script looks for fulfilment text and entities contained in the user sentence, taken as parameter.
# If there are entities (even better if the entities are contained in the fulfilment text), an insertion procedure
# is started. 4 different methods can be chosen to perform the insertion.
import csv
import random
from owlready2 import *
from analyze_text import split_send_dialogflow
from googleNL import entity_analysis
from googleNL import sentiment_analysis
from preprocess_text import lemmatize
from collections import Counter
from PyDictionary import PyDictionary
from topics2 import find_matching_topics
import socket
import os
import glob

path = os.getcwd()
os.chdir("../master_thesis")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'caresses-nlp-3b12fdd574b1.json'

onto = get_ontology("ontology/CKB_new.owl")
onto.load()

test = True

method_fft = 4
method_entity = 4
df_max_words = 4
entity_only = True
ent_types_priority = ["WORK_OF_ART", "LOCATION", "PERSON", "ORGANIZATION", "CONSUMER_GOOD", "EVENT", "OTHER", "UNKNOWN"]

# Global variable filled whenever the user says an additional sentence about a new concept
inserted_sentence = ''
# Positive sentence associated with the individual belonging to an existing class (if the user says yes)
topic_sent = ''

# Variables for method 3:
# Defines the maximum number of synonyms asked to the user
max_synonyms = 2
# If true, the systems asks for subclasses of the class corresponding to the definition (or synonym)
tree_descend = True
# To keep track of the hierarchy of concepts during the insertion with definitions
hierarchy = []

# Keyword 1 corresponding to fulfillment text and entity to be put as property of the new concept in the ontology
keyword1 = []

# Variables for method 4:
# List of classes that the user discarded during the insertion procedure with category method - do not ask for
# classes that are subclasses of these
discarded_classes = []


# This function takes the sentence and adds it as a property of the individual
def add_additional_info(instance, sentence):
    print("...adding additional info to", instance)
    with onto:
        if sentiment_analysis(sentence) >= 0:
            instance.hasPositiveSentence.append(locstr(sentence.rstrip(), lang="en"))
            print("...positive sentence:", instance.hasPositiveSentence)
        else:
            instance.hasNegativeSentence.append(locstr(sentence.rstrip(), lang="en"))
            print("...negative sentence:", instance.hasNegativeSentence)
    onto.save(file="ontology/CKB_new.owl", format="rdfxml")


# Adds the concept to the ontology as son of the parent class
def add_class_to_ontology(concept, parent_class):
    non_existing_parent_class = False
    if ' ' in parent_class or parent_class[0].islower():
        parent_class = parent_class.title().replace(' ', '')
    if ' ' in concept or concept[0].islower():
        concept = concept.title().replace(' ', '')
    with onto:
        try:
            NewClass = types.new_class(concept, (onto[parent_class],))
        except:
            non_existing_parent_class = True
    if non_existing_parent_class:
        print("...non existing parent class, switch to brutal method")
        brutal_method(parent_class, sock)
    else:
        onto.save(file="ontology/CKB_new.owl", format="rdfxml")
        print("...added", concept, "as son of", parent_class)
        send_sentence("Got it! From now on I will remember what " + concept + " is!", sock)
        return NewClass


# This function creates and returns the individual belonging to the class passed as parameter
def add_individual_to_ontology(concept, new_class):
    indiv = "SEN_" + concept.upper().replace(' ', '')
    print(indiv)
    # Create the instance of the individual of that class
    instance = new_class(indiv)
    # Add the isNew property to recognize new individuals
    instance.isNew = [True]
    # Add keyword1 and keyword2 properties - keyword 2 is always *
    print("...adding properties hasKeyword1 and hasKeyword2")
    print (keyword1)
    print (instance.hasKeyword1)
    instance.hasKeyword1=instance.hasKeyword1+keyword1
    instance.hasKeyword2 = [locstr("*", lang="en")]
    instance.hasQuestion.append(locstr(("Do you like "+ instance.hasKeyword1[0] + "?"), lang="en"))
    # Initialize a variable needed to stop the iteration when SEN_GEN individual is found
    found = False
    for cls in list(onto.classes()):
        if found:
            break
        for ind in cls.instances():
            if found:
                break
            # When SEN_GEN individual is found, add the property hasTopic with value the name of the new individual
            if ind.name == "SEN_GEN":
                ind.hasTopic.append(instance)
                print("...added hasTopic property with value: ", instance.name)
                found = True
    onto.save(file="ontology/CKB_new.owl", format="rdfxml")

    return instance


# This function asks the user if the text/entity extracted is correct and if the user wants to add it
def ask_confirmation(concept, sock):
    question = "Did you say " + concept + "?"
    answer = acquire_answer(question, False, sock)
    if "yes" in answer:
        question = "Do you want me to remember the word " + concept + "?"
        answer = acquire_answer(question, False, sock)
    else:
        send_sentence("Ok, sorry I misunderstood.", sock)
        return False
    if "yes" in answer:
        send_sentence("Ok, I will need your help to understand what " + concept + " means.", sock)
        return True
    else:
        send_sentence("Ok, I won't remember it.", sock)
        return False


# On the basis of the value of hasEntityType property, finds the class associated to that entity type
def find_entry_class(ent_type):
    print("...looking for the class associated to entity type", ent_type)
    for ind in list(onto.individuals()):
        for p in list(ind.get_properties()):
            if p.name == "hasEntityType":
                if ind.hasEntityType == ent_type:
                    print("...found corresponding individual:", ind.name)
                    print(ind.is_a)
                    return retrieve_individual_class(ind.name).name


# This function adds the class to the ontology, then asks a sentence about that concept and it adds it to the
# corresponding individual.
def new_concept_addition_procedure(concept, parent_class, sock):
    concept = concept.title().replace(' ', '')
    NewClass = add_class_to_ontology(concept, parent_class)
    instance = add_individual_to_ontology(concept, NewClass)
    # Transform concept in annotation name
    concept = re.sub(r'(?<!^)(?=[A-Z])', ' ', concept).lower()
    print("...added annotation: ",  concept)
    NewClass.comment = "_" + concept
    global inserted_sentence
    if inserted_sentence != '':
        answer = inserted_sentence
    else:
        rand = random.randint(1, 3)
        if rand == 1:
            question = "Great! Please, tell me a sentence about " + concept
        elif rand == 2:
            question = "Please, tell me something about " + concept
        else:
            question = "I would like to know more about what " + concept + " is. Please describe it with a sentence."
        answer = acquire_answer(question, True, sock)
    add_additional_info(instance, answer)


# Recursive method of insertion: try to insert the concept starting from the class passed as parameter
def recursive_insertion(concept, start_class, sock):
    print("...recursive insertion")
    global hierarchy
    global topic_sent
    start_class_annotation, annotated_subclasses, subclasses_annotations = retrieve_annotated_subclasses(start_class)
    # If among the subclasses of the start class, there are annotated subclasses (the name is present)
    if annotated_subclasses:
        for j in range(len(annotated_subclasses)):
            question = ''
            if topic_sent != '':
                question = topic_sent + "\n"
            rand = random.randint(1, 3)
            if rand == 1:
                question = question + "Is " + concept + " a type of " + str(subclasses_annotations[j]) + "?"
            elif rand == 2:
                question = question + "Can I say that " + concept + " is a type of " + \
                           str(subclasses_annotations[j]) + "?"
            else:
                question = question + "Would it be correct to say that " + concept + " is a type of " + \
                           str(subclasses_annotations[j]) + "?"
            answer = acquire_answer(question, False, sock)
            if "yes" in answer:
                topic_sent = sentence_about_correct_class(str(subclasses_annotations[j]))
                # print("...topic sentence: ", topic_sent)
                recursive_insertion(concept, annotated_subclasses[j], sock)
                return
            else:
                topic_sent = ''
                if j == len(annotated_subclasses)-1:
                    question = "Ok...so, have I understood correctly that " + concept + " is a type of " + \
                               str(start_class_annotation) + "?"
                    answer = acquire_answer(question, False, sock)
                    if "yes" in answer:
                        new_concept_addition_procedure(concept, start_class, sock)
                        if hierarchy:
                            print(hierarchy)
                            for i in range(len(hierarchy) - 1):
                                new_concept_addition_procedure(hierarchy[i + 1], hierarchy[i], sock)
                        print("returning")
                        return
                    else:
                        topic_sent = ''
                        if start_class == "Topic":
                            send_sentence("Ok, I will not remember it.", sock)
                            return
                        send_sentence("Ok, then I will ask you some more questions...", sock)
    else:
        if start_class_annotation:
            question = ''
            if topic_sent != '':
                question = topic_sent + "\n"
            rand = random.randint(1, 3)
            if rand == 1:
                question = question + "Do you want to add " + concept + " as a type of " + str(start_class_annotation) + "?"
            elif rand == 2:
                question = question + "You want me to learn that " + concept + " is a type of " + str(start_class_annotation) + "?"
            else:
                question = question + "Do you want me to remember that " + concept + " is a type of " \
                           + str(start_class_annotation) + "?"

            answer = acquire_answer(question, False, sock)
            if "yes" in answer:
                new_concept_addition_procedure(concept, start_class, sock)
                if hierarchy:
                    for i in range(len(hierarchy) - 1):
                        print("...hierarchy: ", hierarchy)
                        new_concept_addition_procedure(hierarchy[i + 1], hierarchy[i], sock)
                return
            else:
                topic_sent = ''
                # Return to previous level of the tree
                send_sentence("Oh, I would like to understand what ", concept, " is...", sock)
        else:
            print("...no annotations found - switch to brutal method")
            brutal_method(concept, sock)


# This function looks for all the subclasses of a given class that are contain an annotation starting with _
# Returns the annotation of the start class (if exists), a list containing all annotated subclasses and a
# list containing all the corresponding annotations
def retrieve_annotated_subclasses(start_class):
    if start_class[0].islower():
        start_class = start_class.title().replace(' ', '')
    print("...retrieving annotations for", start_class, "and its subclasses")
    subclasses = retrieve_subclasses(start_class)
    print("...subclasses:", subclasses)
    annotated_subclasses = []
    subclasses_annotations = []
    start_class_annotation = []
    # In case the start class has no subclasses, in this way I can retrieve its annotation (if exists)
    if not subclasses:
        for cls in onto.classes():
            if cls.name == start_class and cls.comment:
                for com in cls.comment:
                    if '_' in com:
                        start_class_annotation = com.replace('_', '')
    else:
        for subclass in subclasses:
            for cls in onto.classes():
                if cls.name == start_class and cls.comment:
                    for com in cls.comment:
                        if '_' in com:
                            start_class_annotation = com.replace('_', '')
                if cls.name == subclass and cls.comment:
                    for com in cls.comment:
                        if '_' in com:
                            annotated_subclasses.append(subclass)
                            subclasses_annotations.append(com.replace('_', ''))
    print("...start class annotation: ", start_class_annotation)
    print("...annotated subclasses:", annotated_subclasses)
    print("...subclasses annotations:", subclasses_annotations)
    return start_class_annotation, annotated_subclasses, subclasses_annotations


# This function returns the class of the individual passed as argument
def retrieve_individual_class(indiv):
    print("...looking for", indiv, "class")
    indiv_cls = []
    for cls in list(onto.classes()):
        for instance in cls.instances():
            if instance.name == indiv:
                indiv_cls = instance.is_a
                # print("found class:", indiv_cls)
                break
    if not indiv_cls:
        print("...no class found - check individual name in the ontology!")
        return []
    else:
        return indiv_cls[0]


# This function returns the list of subclasses of a given class
def retrieve_subclasses(parent_class):
    print("...retrieving subclasses of", parent_class)
    subcls = []
    for cls in list(onto.classes()):
        if cls.name == parent_class:
            for subclass in list(cls.subclasses()):
                subcls.append(subclass.name)
    return subcls


# Order entities on the basis of the defined priorities
def order_entities(entities, ent_types):
    ordered_ent = []
    ordered_ent_types = []
    for ent_ty in ent_types_priority:
        for j in range(len(ent_types)):
            if ent_types[j] == ent_ty:
                # Save ordered entities in array
                ordered_ent.append(entities[j])
                ordered_ent_types.append(ent_types[j])
    print("Ordered entities: ", ordered_ent)
    return ordered_ent, ordered_ent_types


# This function returns (if exists) the fulfilment text that contains the ent with the highest priority,
# along with its associated intent, the ent/entities contained and their types.
# If no fft contains entities but there are entities, return them ordered.
# If there are no entities but there is a small talk, return it.
def pick_best_solution(fulf_texts, intents, entities, ent_types):
    ord_ents, ord_ents_type = order_entities(entities, ent_types)
    for j in range(len(ord_ents)):
        for k in range(len(fulf_texts)):
            if intents[k]:
                # if there is an intent and there is a fulfilment text
                if fulf_texts[k] and fulf_texts[k] != ':':
                    # Check that its length is inferior to the max
                    if len(fulf_texts[k].split()) < df_max_words+1:
                        # Take only the part after ':'
                        splitted_fft = fulf_texts[k].split(':')[1]
                        if ord_ents[j] in splitted_fft:
                            return splitted_fft, intents[k], ord_ents[j], ord_ents_type[j]
            else:
                # If there is no intent but the fulfilment text exists and does not contain ':'
                if fulf_texts[k] and ':' not in fulf_texts[k]:
                    return fulf_texts[k], [], [], []
    # If there are no entities
    if not entities or not ord_ents:
        for k in range(len(fulf_texts)):
            if fulf_texts[k] and not intents[k]:
                return fulf_texts[k], [], [], []
        # If there is no entities (or the entity type is not in the priority list) and no small talk return empty
        return [], [], [], []
    # If there are entities (but none is contained in ffts, return the highest priority ent and its type

    return [], [], ord_ents[0], ord_ents_type[0]


# This function checks if the class of the individual (returned by topics2) is one of the already discarded classes
# or if it is a subclass of a discarded class = the user said no.
def check_if_subclass_of_discarded_classes(indiv_class):
    global discarded_classes
    if indiv_class in discarded_classes:
        return True
    for disc_cls in discarded_classes:
        for cls in list(onto.classes()):
            if cls.name == disc_cls:
                subclasses = retrieve_subclasses(cls.name)
                if indiv_class in subclasses:
                    return True
    return False


# METHOD 1: Starts from the top of the ontology and scans all class
def brutal_method(concept, sock):
    print("\nMETHOD 1: Brutal")
    if concept[0].isupper():
        concept = re.sub(r'(?<!^)(?=[A-Z])', ' ', concept).lower()
    recursive_insertion(concept, "Topic", sock)


# METHOD 2: Starts from the class associated to the entity type (if exists, otherwise brutal method)
def entity_type_method(ent, ent_type, sock):
    print("\nMETHOD 2: Entity Type")
    global topic_sent
    entry_class = find_entry_class(ent_type)
    if entry_class:
        start_class_annotation, _, _ = retrieve_annotated_subclasses(entry_class)
        # If the annotation of the starting class exists (should always exist for those classes)...
        if start_class_annotation:
            # Ask if the class associated to the ent is correct
            question = "Is " + ent + " a type of " + str(start_class_annotation) + "?"
            answer = acquire_answer(question, False, sock)
            if "yes" in answer:
                topic_sent = sentence_about_correct_class(entry_class)
                print("...topic sentence: ", topic_sent)
                recursive_insertion(ent, entry_class, sock)
            else:
                topic_sent = ''
    # If the entry class does not exist, or the user says that the concept is not a person/location ecc
    # start with brutal method
    brutal_method(ent, sock)


# METHOD 3: Asks the user what is that concept - if the definition is not in the ontology, it looks for synonyms
def definitions_method(concept, sock):
    global hierarchy
    print("\n METHOD 3: synonyms method")
    # Ask the user a simple sentence which describes what the concept is
    # Transform concept in annotation name
    concept = re.sub(r'(?<!^)(?=[A-Z])', ' ', concept).lower()
    rand = random.randint(1, 3)
    if rand == 1:
        question = "I'm not sure what you are talking about. Please, tell me what is a " + concept + ".\n" \
                    'If you don\'t know how to define it, say "stop"'
    elif rand == 2:
        question = "I'm sorry but I don't know what " + concept + " is. I would be happy if you could define what " \
                    "it is.\n If you are not able to find a suitable definition just tell me to stop."
    else:
        question = "I would be happy if you could give me a definition of " + concept + ". \nIf no definition comes " \
                                                                                        "to your mind, tell me to stop"
    hierarchy = [concept] + hierarchy
    answer = acquire_answer(question, True, sock)
    # If the user doesn't know how to define it, it goes under Topic
    if answer.lower() == "stop":
        new_concept_addition_procedure(concept, "Topic", sock)
        if hierarchy:
            for i in range(len(hierarchy) - 1):
                print(hierarchy)
                new_concept_addition_procedure(hierarchy[i + 1], hierarchy[i], sock)
        return
    fulf_texts, intents = split_send_dialogflow(answer)
    print("fulfilment text: ", fulf_texts)
    # I expect that there is only one fulfilment text because the sentence is small (consider only the first)
    # in case it is a small talk answer containing only :, ignore it
    if fulf_texts[0] and fulf_texts[0] != ':':
        if intents[0]:
            fulf_text = fulf_texts[0].split(':')[1]
            print("...relevant part:", fulf_text)
            # recursive_definition_check(concept, fulf_text, sock)
            recursive_synonym_check(concept, fulf_text, sock)
        # Small talk - print and exit (OK?)
        else:
            print(fulf_texts[0])
            return
    # If nothing is recognized, start brutal method
    else:
        brutal_method(concept, sock)


# METHOD 4: Asks the user a sentence with that concept, then looks for the category and finds the topic with
# highest match - if more are present, then look for the highest in the dialogue tree - if more, random
def category_method(concept, sock):
    global inserted_sentence
    global topic_sent
    print("\n METHOD 4: sentence category")
    question = "Please, tell me a sentence about " + concept + " to help me understand what it is"
    inserted_sentence = acquire_answer(question, True, sock)
    ordered_topics_numbers = find_matching_topics(inserted_sentence)
    print("RETURNED ordered topics: ", ordered_topics_numbers)
    # If there are matching topics
    if ordered_topics_numbers:
        # If there is only one topic, it's just an int
        if type(ordered_topics_numbers) == int:
            ordered_topics_numbers = [ordered_topics_numbers]
        # Otherwise it means there is more than one topic and it is an array - for each one try the insertion
        for topic_number in ordered_topics_numbers:
            print("Discarded classes: ", discarded_classes)
            indiv = find_topic_individual(topic_number)
            try:
                indiv_class = retrieve_individual_class(indiv).name
            except:
                break
            print(indiv_class)
            if check_if_subclass_of_discarded_classes(indiv_class):
                pass
            start_class_annotation, _, _ = retrieve_annotated_subclasses(indiv_class)
            # If the annotation of the starting class exists (should always exist for those classes)...
            if start_class_annotation:
                # Ask if the class associated to the ent is correct
                question = "Is " + concept + " a type of " + str(start_class_annotation) + "?"
                answer = acquire_answer(question, False, sock)

                if "yes" in answer:
                    topic_sent = sentence_about_correct_class(indiv_class)
                    print("...topic sentence: ", topic_sent)
                    recursive_insertion(concept, indiv_class, sock)
                    return
                else:
                    topic_sent = ''
                discarded_classes.append(indiv_class)
    print("...no topics found or no more topics to ask for correctness...")
    brutal_method(concept, sock)


# METHOD FOR TESTING
def random_method(concept, sock):
    global inserted_sentence
    inserted_sentence = "TEST"
    random_class = random.choice(list(onto.classes())).name

    new_concept_addition_procedure(concept, random_class, sock)


# Ask a definition to the user, if the class exists add the concept, otherwise ask what is it...
def recursive_definition_check(concept, fulf_text, sock):
    global hierarchy
    global topic_sent
    print("...recursive definition check!")
    if check_concept_existence(fulf_text):
        question = ''
        if topic_sent != '':
            question = topic_sent + "\n"
        rand = random.randint(1, 3)
        if rand == 1:
            question = question + "Is " + concept + " a type of " + fulf_text + "?"
        elif rand == 2:
            question = question + "Is it correct to say that " + concept + " is a type of " + fulf_text + "?"
        else:
            question = question + "Would you say that " + concept + " is a type of " + fulf_text + "?"
        answer = acquire_answer(question, False, sock)
        if "yes" in answer:
            topic_sent = sentence_about_correct_class(fulf_text)
            print("...topic sentence: ", topic_sent)
            perform_insertion(concept, fulf_text, sock)
            return
        else:
            topic_sent = ''
            brutal_method(concept, sock)
    else:
        definitions_method(fulf_text, sock)


# If the definition given by the user is not a class, try looking for synonyms
def recursive_synonym_check(concept, fulf_text, sock):
    global hierarchy
    global topic_sent
    print("...recursive synonyms check")
    fulf_annotation = []
    if check_concept_existence(fulf_text):
        fulf_annotation, _, _ = retrieve_annotated_subclasses(fulf_text)
    if fulf_annotation:
        question = ''
        if topic_sent != '':
            question = topic_sent + "\n"
        rand = random.randint(1, 3)
        if rand == 1:
            question = question + "Is " + concept + " a type of " + str(fulf_annotation) + "?"
        elif rand == 2:
            question = question + "Is it correct to say that " + concept + " a type of " + \
                       str(fulf_annotation) + "?"
        else:
            question = question + "Would you say that " + concept + " is a type of " + str(fulf_annotation) + "?"
        answer = acquire_answer(question, False, sock)
        if "yes" in answer:
            topic_sent = sentence_about_correct_class(fulf_text)
            print("...topic sentence: ", topic_sent)
            perform_insertion(concept, fulf_text, sock)
            return
        else:
            topic_sent = ''
            brutal_method(concept, sock)
    # If the concept does not correspond to any class in the ontology, look for synonyms
    else:
        fulf_text = fulf_text.replace(' ', '')
        print("...looking for synonyms of ", fulf_text)

        # Synonyms with PyDictionary
        dictionary = PyDictionary()
        # For each synonym check if it exists in the ontology, if it does ask confirmation and add it.
        # Ask for a maximum of max_synonyms - otherwise it becomes boring
        # Initialize a variable to keep count of how many synonyms (which have a corresponding class) I have asked
        asked_synonyms = 0
        if dictionary.synonym(fulf_text):
            for syn in dictionary.synonym(fulf_text):
                # If I have reached the maximum number of synonyms asked, go ahead and ask again for a definition
                if asked_synonyms == max_synonyms:
                    break
                if check_concept_existence(syn):
                    syn_annotation, _, _ = retrieve_annotated_subclasses(syn)
                    if asked_synonyms == max_synonyms or not syn_annotation:
                        break

                    question = ''
                    if topic_sent != '':
                        question = topic_sent + "\n"
                    rand = random.randint(1, 3)
                    if rand == 1:
                        question = question + "Is " + concept + " a type of " + str(syn_annotation) + "?"
                    elif rand == 2:
                        question = question + "Is it correct to say that " + concept + " is a type of " \
                                   + str(syn_annotation) + "?"
                    else:
                        question = question + "Would it be correct to say that " + concept + " is a type of " \
                                   + str(syn_annotation) + "?"

                    answer = acquire_answer(question, False, sock)
                    if "yes" in answer:
                        topic_sent = sentence_about_correct_class(fulf_text)
                        print("...topic sentence: ", topic_sent)
                        perform_insertion(concept, syn, sock)
                        return
                    else:
                        topic_sent = ''
                    asked_synonyms += 1
        definitions_method(fulf_text, sock)


# Function called by the recursive definition or synonym procedure when a definition/synonym is found
def perform_insertion(concept, start_class, sock):
    global hierarchy
    if tree_descend:
        # If the flag is true, check also for subclasses
        recursive_insertion(concept, start_class, sock)
    else:
        new_concept_addition_procedure(concept, start_class, sock)
        for i in range(len(hierarchy) - 1):
            new_concept_addition_procedure(hierarchy[i + 1], hierarchy[i], sock)


# Checks if the concept already exists in the ontology
def check_concept_existence(concept):
    concept = concept.title().replace(' ', '')
    print("...checking if", concept, "exists")
    for cls in onto.classes():
        if cls.name == concept:
            print("...already existing concept", cls.name, "\n")
            return True
    print("...No matches found - proceed with confirmation")
    return False


def pick_highest_indiv_in_tree(individuals):
    # print(individuals)
    print("Find the highest one in the dialogue tree")
    file = open("csv/resume_tree.csv", 'r')
    lines = file.readlines()
    indiv_tabs = []
    for indiv in individuals:
        found = False
        for line in lines:
            # When you find the first one, pass to the next individual otherwise the indexes will be biased
            if found:
                break
            if indiv in line:
                found = True
                # print(line)
                count = Counter(line)
                tabs = count["\t"]
                indiv_tabs.append(tabs)
    lowest_tab = min(indiv_tabs)
    # If there are more topics at the highest level choose randomly
    if indiv_tabs.count(lowest_tab) > 1:
        indexes = []
        for i in range(len(indiv_tabs)):
            if indiv_tabs[i] == lowest_tab:
                indexes.append(i)
        print("Indexes of elements with lowest tabs: ", indexes)
        return individuals[random.choice(indexes)]
    # If there is only one topic at the highest level, choose that
    else:
        return individuals[indiv_tabs.index(lowest_tab)]


# This function retrieves the topic of the individual passed as parameter in every form (SEN_A_B, A_B, AB)
def find_individual_topic(indiv):
    csv_input = open('csv/resume.csv', 'r')
    for row in csv.reader(csv_input):
        # check if the topic in the csv is among those
        if row[0] == indiv or row[5] == indiv or ("SEN_" + row[5]) == indiv:
            print(type(row[1]))
            return row[1]
    return -1


def find_topic_individual(topic_n):
    print("...looking for topic", topic_n, "individual")
    csv_input = open('csv/resume.csv', 'r')
    for row in csv.reader(csv_input):
        # check if the topic in the csv is among those
        if row[1] == str(topic_n):
            return "SEN_" + row[5]


def retrieve_existing_concept_topic(concept):
    print("...retrieving individuals of", concept, "...")
    concept = concept.title().replace(' ', '')
    individuals = []
    for cls in onto.classes():
        if cls.name == concept:
            for inst in cls.instances():
                if "SEN_" in inst.name:
                    # Add to array the name of the individual without SEN
                    individuals.append(inst.name.replace('_', '')[3:])
    # If there is only one individual there is no point in checking which is the highest in the tree.
    if len(individuals) == 1:
        print("Only one individual:", individuals[0])
        highest_indiv = individuals[0]
    else:
        highest_indiv = pick_highest_indiv_in_tree(individuals)
    print("Highest individual:", highest_indiv)
    print("Returning associated topic number:", find_individual_topic(highest_indiv))
    return find_individual_topic(highest_indiv)


def insertion_routine(method, new_concept, entity_type, fulf_texts, intents, entities, entity_types, sock):
    # Check if the concept already exists: if not, go ahead with the insertion
    if not check_concept_existence(new_concept):
        confirm = ask_confirmation(new_concept, sock)
        if confirm:
            if method == 1:
                brutal_method(new_concept, sock)
            elif method == 2:
                entity_type_method(new_concept, entity_type, sock)
            elif method == 3:
                definitions_method(new_concept, sock)
            elif method == 4:
                category_method(new_concept, sock)
            else:
                print("Non-existing method, specify a number between 1 and 4")
        return
    # If the concept already exists, there is a class in the ontology with an associated individual and topic
    else:
        method = random.randint(1, 2)
        # The first method consists in retrieving the topic of the class
        if method == 1:
            print("Look for the topic associated to the highest individual in dialogue tree of", new_concept)
            retrieve_existing_concept_topic(new_concept)
            return
        # The second method consists in retrieving another entity - DELETE considered entity/fft
        print("Look for other entities/fft (respecting priorities)")
        if new_concept in fulf_texts:
            index = fulf_texts.index(new_concept)
            del fulf_texts[index]
            del intents[index]
        if new_concept in entities:
            index = entities.index(new_concept)
            del entities[index]
            del entity_types[index]
        start_procedure(fulf_texts, intents, entities, entity_types, sock)


def start_procedure(fulf_texts, intents, entities, entity_types, sock):
    # Choose the best fft containing the highest priority entity
    # If no fft contains an entity, but there are entities, return the highest priority one and its type.
    # If there are no entities and there is a small talk, return it as fft.
    fulf_text, intent, ent, entity_type = pick_best_solution(fulf_texts, intents, entities, entity_types)

    if fulf_text:
        if intent:
            print("...fft before lemmatization:", fulf_text)
            fulf_text = lemmatize(fulf_text)
            print("...fft after lemmatization:", fulf_text)

            keyword1.append(locstr(fulf_text, lang="en"))
            keyword1.append(locstr(ent, lang="en"))
            print("...keyword 1: ", keyword1)
            # 1 Brutal, 2 Entity type, 3 Definition + Synonyms, 4 Category
            insertion_routine(method_fft, fulf_text, entity_type, fulf_texts, intents, entities, entity_types, sock)
        # If there is the fulfilment text but there is no intent -> small talk
        print(fulf_text)
        return
    else:
        # If the procedure with only entities not in fft is allowed
        if entity_only:
            print("Entity-only procedure")
            # If there is no fulfilment text but there is an entity, it is the highest priority one.
            if ent:
                # No fft but entities present - extract higher priority one
                print("...entity before lemmatization:", ent)
                ent = lemmatize(ent)
                print("...entity after lemmatization:", ent)
                keyword1.append(locstr(ent, lang="en"))

                # 1 Brutal, 2 Entity type, 3 Definition + Synonyms, 4 Category
                insertion_routine(method_entity, ent, entity_type, fulf_texts, intents, entities, entity_types, sock)
            # No entities and no fft (no small talk)
            else:
                print("No entities! (and no small talk)")
                return
        print("Entity-only procedure: not allowed")
        return


def send_sentence(sentence, mysock):
    sentence = sentence.replace('_', ' ')
    sstring = sentence+"\n"
    mysock.sendall(sstring.encode())


def acquire_answer(question, flag, mysock):
    question = question.replace('_', ' ')
    sstring = question+"#"+str(flag)+"\n"
    mysock.sendall(sstring.encode())
    rec = mysock.recv(1024)
    rec = rec.decode("utf-8")
    return rec


def connect_to_server():
    server_address = ("127.0.0.1", 1050)
    sock.connect(server_address)


def retrieve_individual_of_given_class(cls):
    indivs = []
    for indiv in onto.individuals():
        # print(cls)
        # print(indiv.is_a[0].name)
        if indiv.is_a[0].name == cls:
            if "SEN_" in indiv.name:
                # print("Found individual! -> ", indiv)
                if indiv.name not in indivs:
                    # indivs.append(indiv.name.replace('_', '')[3:])
                    indivs.append(indiv.name)

    print("...individuals of class ", cls, ": ", indivs)
    # If there is only one individual there is no point in checking which is the highest in the tree.
    if indivs:
        return random.choice(indivs)
    return ''


# This function returns a sentence associated to the topic of the individual belonging to the class
def sentence_about_correct_class(cls):
    print("...retrieving sentence associated to class individual")
    if cls[0].islower():
        cls = cls.title().replace(' ', '')
    topic = retrieve_individual_of_given_class(cls)
    print(topic)
    if topic != '':
        topic_n = int(find_individual_topic(topic))
    else:
        topic_n = -1
    # print("...topic number: ", topic_n)

    thr = 1000000
    number = -1

    for file in glob.glob('../CKB_new/topic*.enu'):
        a = int(file.split("topic")[1].split(".enu")[0])
        min = topic_n - a
        if min >= 0 and min < thr:
            thr = min
            number = a

    if number == -1:
        return ''
    else:
        file = open("../CKB_new/topic" + str(number) + ".enu", 'r')

    lines = file.readlines()
    pos_sentences = []
    for line in lines:
        if str(topic_n) in line and '#p' in line:
            pos_sentences.append(line.split(':')[1].split('#')[0])
    return random.choice(pos_sentences)

def main(argv):
    text = argv[1]
    #text = "I love apples"
    text = text.replace('_', ' ')
    # text_len = len(text.split())
    print(text)

    connect_to_server()

    # call the function which splits the text and sends each part to df -> returns each fft and intent
    fulf_texts, intents = split_send_dialogflow(text)
    entities, entity_types = entity_analysis(text)

    # When more than one concept is recognized in one fft, they are joined with an and -> separate them in two
    # different ffts and add the second one at the end of the array with its relative intent.
    for i in range(len(fulf_texts)):
        if "and" in fulf_texts[i]:
            fulf_texts[i], splitted = fulf_texts[i].split("and")
            fulf_texts.append(fulf_texts[i].split(':')[0] + ':' + splitted)
            intents.append(intents[i])

    print("----------DF----------")
    for i in range(len(fulf_texts)):
        print("Fulfilment text:", fulf_texts[i])
        print("Intent:", intents[i])

    print("----------NL----------")
    print("Entities:", entities)
    print("Types:", entity_types)
    print("\n")

    start_procedure(fulf_texts, intents, entities, entity_types, sock)
    print("finefine")

if __name__ == '__main__':
    main(sys.argv)
