from owlready2 import *


def retrieve_subclasses(ontology: Ontology, parent_class: str) -> list:
    subcls = []
    for cls in list(ontology.classes()):
        if cls.name == parent_class:
            for subclass in list(cls.subclasses()):
                subcls.append(subclass.name)
    return subcls


# Adds the concept to the ontology as son of the parent class
def add_class_to_ontology(ontology: Ontology, ontologyPath: str, concept: str, parent_class: str) -> None:
    if ' ' in parent_class or parent_class[0].islower():
        parent_class = parent_class.title().replace(' ', '')
    if ' ' in concept or concept[0].islower():
        concept = concept.title().replace(' ', '')
    with ontology:
        types.new_class(concept, (ontology[parent_class],))
    ontology.save(file=ontologyPath, format="rdfxml")


def add_hasSentece_child_data_property(ontology: Ontology, ontologyPath: str, instance, sentence: str, \
                                       type: int, questionFlag: int, answer: str = "NULL") -> None:
    print("...adding additional info to", instance)  # to be deleted
    with ontology:
        if questionFlag == 0:
            if type == 0:
                instance.hasPositiveSentence.append(locstr(sentence.rstrip(), lang="en"))
            elif type == 1:
                instance.hasNegativeSentence.append(locstr(sentence.rstrip(), lang="en"))
            else:
                instance.hasPositiveAndWait.append(locstr(sentence.rstrip(), lang="en"))
        else:
            if type == 0:
                instance.hasQuestion.append(locstr(sentence.rstrip(), lang="en"))
            elif type == 1:
                instance.hasQuestionGoal.append(locstr(sentence.rstrip(), lang="en"))
            else:
                instance.hasQuestionContextual.append(locstr(sentence.rstrip(), lang="en"))
                #remember the answer here
    ontology.save(file=ontologyPath, format="rdfxml")
