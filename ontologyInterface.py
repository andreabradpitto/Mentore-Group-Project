from owlready2 import *


# Returns all the subclasses of a given parent class
def retrieve_subclasses(ontology: Ontology, parent_class: str) -> list:
    subcls = []
    for cls in list(ontology.classes()):
        if cls.name == parent_class:
            for subclass in list(cls.subclasses()):
                subcls.append(subclass.name)
    return subcls


# This function creates and returns the individual belonging to the class passed as parameter
#def add_individual_to_ontology(concept, new_class):
#    indiv = "SIN_" + concept.upper().replace(' ', '')
#    print(indiv)
#    # Create the instance of the individual of that class
#    instance = new_class(indiv)
#    # Add the isNew property to recognize new individuals
#    instance.isNew = [True]
#    # Add keyword1 and keyword2 properties - keyword 2 is always *
#    print("...adding properties hasKeyword1 and hasKeyword2")
#    print (keyword1)
#    print (instance.hasKeyword1)
#    instance.hasKeyword1=instance.hasKeyword1+keyword1
#    instance.hasKeyword2 = [locstr("*", lang="en")]
#    instance.hasQuestion.append(locstr(("Do you like "+ instance.hasKeyword1[0] + "?"), lang="en"))
#    # Initialize a variable needed to stop the iteration when SEN_GEN individual is found
#    found = False
#    for cls in list(onto.classes()):
#        if found:
#            break
#        for ind in cls.instances():
#            if found:
#                break
#            # When SEN_GEN individual is found, add the property hasTopic with value the name of the new individual
#            if ind.name == "SIN_GEN":
#                ind.hasTopic.append(instance)
#                print("...added hasTopic property with value: ", instance.name)
#                found = True
#    onto.save(file="ontology/CKB_new.owl", format="rdfxml")

    return instance


# Returns the class with the corresponding inputted name
def retrieve_class(ontology: Ontology, class_name: str):
    for cls in list(ontology.classes()):
        if cls.name == class_name:
            return cls


# Adds the concept to the ontology as son of the parent class
def add_class_to_ontology(ontology: Ontology, ontologyPath: str, concept: str, parent_class: str) -> None:
    if ' ' in parent_class or parent_class[0].islower():
        parent_class = parent_class.title().replace(' ', '')
    if ' ' in concept or concept[0].islower():
        concept = concept.title().replace(' ', '')
    with ontology:
        types.new_class(concept, (ontology[parent_class],))
    ontology.save(file=ontologyPath, format="rdfxml")


# Adds a sentence or a question to the hasSentence data property of the class whose name matches the inputted string
def add_hasSentece_data_property(ontology: Ontology, ontologyPath: str, active_class_name: str, sentence: str,
                                 data_type: int, questionFlag: int, answer: str = "NULL") -> None:
    with ontology:
        active_class = retrieve_class(
            ontology, active_class_name)

        if questionFlag == 0:
            if data_type == 0:
                active_class.hasPositiveSentence_4.append(
                    locstr(sentence.rstrip(), lang="en"))
            elif data_type == 1:
                active_class.hasNegativeSentence_4.append(
                    locstr(sentence.rstrip(), lang="en"))
            else:
                active_class.hasPositiveAndWait_4.append(
                    locstr(sentence.rstrip(), lang="en"))
        else:
            if data_type == 0:
                active_class.hasQuestion_4.append(
                    locstr(sentence.rstrip(), lang="en"))
            elif data_type == 1:
                active_class.hasQuestionGoal_4.append(
                    locstr(sentence.rstrip(), lang="en"))
            else:
                active_class.hasQuestionContextual_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_class.hasQuestionContextualReply_4.append(
                    locstr(answer.rstrip(), lang="en"))
    ontology.save(file=ontologyPath, format="rdfxml")
