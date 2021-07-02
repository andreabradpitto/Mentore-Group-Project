from owlready2 import *


# Returns all the subclasses of a given parent class
def retrieve_subclasses(ontology: Ontology, parent_class: str) -> list:
    subcls = []
    for cls in list(ontology.classes()):
        if cls.name == parent_class:
            for subclass in list(cls.subclasses()):
                subcls.append(subclass.name)
    return subcls


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
                active_class.hasPositiveSentence.append(
                    locstr(sentence.rstrip(), lang="en"))
            elif data_type == 1:
                active_class.hasNegativeSentence.append(
                    locstr(sentence.rstrip(), lang="en"))
            else:
                active_class.hasPositiveAndWait.append(
                    locstr(sentence.rstrip(), lang="en"))
        else:
            if data_type == 0:
                active_class.hasQuestion.append(
                    locstr(sentence.rstrip(), lang="en"))
            elif data_type == 1:
                active_class.hasQuestionGoal.append(
                    locstr(sentence.rstrip(), lang="en"))
            else:
                active_class.hasQuestionContextual.append(
                    locstr(sentence.rstrip(), lang="en"))
                active_class.hasQuestionContextualReply.append(
                    locstr(answer.rstrip(), lang="en"))
    ontology.save(file=ontologyPath, format="rdfxml")
