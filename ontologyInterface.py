from os import listxattr
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
    for cls in list(ontology.classes()):
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
    ontology.save(file="ontology/CKB_new.owl", format="rdfxml")
