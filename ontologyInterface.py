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
# and adds a generic sentence via the hasPositiveSentence data property,
# as well as a generic question via the hasQuestion data property
def add_individual_to_ontology(ontology: Ontology, ontologyPath: str, concept: str, new_class):
    indiv = "SIN_" + concept.upper().replace(' ', '')
    # Create the instance of the individual of that class
    instance = new_class(indiv)
    # Add the isNew property to recognize new individuals
    instance.isNew = [True]
    # Add keyword1 and keyword2 properties - keyword 2 is always *
    instance.hasKeyword1 = [
        locstr(concept.lower().replace(' ', ''), lang="en")]
    instance.hasKeyword2 = [locstr("*", lang="en")]
    instance.hasPositiveSentence_4.append(
        locstr(("Let's talk about " + instance.hasKeyword1[0] + "!"), lang="en"))
    instance.hasQuestion_4.append(
        locstr(("Do you want to talk about " + instance.hasKeyword1[0] + "?"), lang="en"))
    # Initialize a variable needed to stop the iteration when SIN_GEN individual is found
    for cls in list(ontology.classes()):
        for ind in cls.instances():
            # When SIN_GEN individual is found, add the property hasTopic with value the name of the new individual
            if ind.name == "SIN_GEN":
                ind.hasTopic.append(instance)
                break
        else:
            continue
        break
    ontology.save(file=ontologyPath, format="rdfxml")
    return instance


# Returns the class with the corresponding inputted name
def retrieve_class(ontology: Ontology, class_name: str):
    for cls in list(ontology.classes()):
        if cls.name == class_name:
            return cls


# Adds the concept to the ontology as son of the parent class and returns the new class
def add_class_to_ontology(ontology: Ontology, ontologyPath: str, concept: str, parent_class: str) -> None:
    if ' ' in parent_class or parent_class[0].islower():
        parent_class = parent_class.title().replace(' ', '')
    if ' ' in concept or concept[0].islower():
        concept = concept.title().replace(' ', '')
    with ontology:
        NewClass = types.new_class(concept, (ontology[parent_class],))
    ontology.save(file=ontologyPath, format="rdfxml")
    return NewClass


# Adds a sentence or a question as a child of the hasSentence data property
# of the class and individual whose names match the inputted string
def add_hasSentece_data_property(ontology: Ontology, ontologyPath: str, active_class_name: str, sentence: str,
                                 data_type: int, questionFlag: int, answer: str = "NULL") -> None:
    with ontology:
        active_class = retrieve_class(
            ontology, active_class_name)

        for cls in list(ontology.classes()):
            for ind in cls.instances():
                if ind.name == "SIN_" + active_class_name.upper():
                    active_individual = ind
                    break
            else:
                continue
            break

        if questionFlag == 0:

            if data_type == 0:
                active_class.hasPositiveSentence_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_individual.hasPositiveSentence_4.append(
                    locstr(sentence.rstrip(), lang="en"))

            elif data_type == 1:
                active_class.hasNegativeSentence_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_individual.hasNegativeSentence_4.append(
                    locstr(sentence.rstrip(), lang="en"))

            else:
                active_class.hasPositiveAndWait_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_individual.hasPositiveAndWait_4.append(
                    locstr(sentence.rstrip(), lang="en"))

        else:

            if data_type == 0:
                active_class.hasQuestion_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_individual.hasQuestion_4.append(
                    locstr(sentence.rstrip(), lang="en"))

            elif data_type == 1:
                active_class.hasQuestionGoal_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_individual.hasQuestionGoal_4.append(
                    locstr(sentence.rstrip(), lang="en"))

            else:
                active_class.hasQuestionContextual_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_class.hasQuestionContextualReply_4.append(
                    locstr(answer.rstrip(), lang="en"))
                active_individual.hasQuestionContextual_4.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_individual.hasQuestionContextualReply_4.append(
                    locstr(answer.rstrip(), lang="en"))

    ontology.save(file=ontologyPath, format="rdfxml")
