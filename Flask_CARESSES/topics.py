import sys
import csv
import random
from topics_utils import get_topics_keywords_and_likelinesses


# This function trims any point, comma or parenthesis, and replaces underscores with spaces
def clean_text(text):
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('_', ' ')
    text = text.lower()
    return text


def retrieve_topic_name(topic_n):
    with open(r'F:\Robotics\Group_Project\BeingAI\Flask_CARESSES\dialogue_tree\resume.csv', 'r') as csv_input:
        for row in csv.reader(csv_input):
            if int(row[1]) == topic_n:
                return row[0]


# This function chooses randomly from the array picking only from the indexes passed as parameter
def choose_topic(topics, likelinesses, allow_zero):
    valid_topics = []
    likelinesses_sum = 0.0
    incremental_likelinesses = []
    for i in range(len(topics)):
        if float(likelinesses[topics[i]]) != 0:
            likelinesses_sum = likelinesses_sum + float(likelinesses[topics[i]])
            incremental_likelinesses.append(likelinesses_sum)
            valid_topics.append(topics[i])
    # If there are topics with likeliness != 0
    if valid_topics:
        # Initialize the chosen topic to the first valid one
        chosen_topic = valid_topics[0]
        print("Valid topics: ", valid_topics)
        print("Incremental likelinesses: ", incremental_likelinesses)

        rand_num = random.uniform(0.0, likelinesses_sum)
        print("Random number chosen:", rand_num)
        for n in range(len(incremental_likelinesses)):
            if incremental_likelinesses[n] < rand_num <= incremental_likelinesses[n + 1]:
                chosen_topic = valid_topics[n + 1]
    # If there are no topics with likeliness != 0
    else:
        # If we can return topics with likeliness 0, choose one randomly
        if allow_zero:
            chosen_topic = random.choice(topics)
        # If we are not allow to consider topics with likeliness 0, return -1
        else:
            chosen_topic = -1
    print("Chosen topic: ", chosen_topic)
    return chosen_topic


def main(text, id_req, likelinesses, req_par1, req_par2, tot_topic):
    if text == " " or text == "_":
        text = "null"
    text = clean_text(text)
    # Find matches of parameters #1
    param1_topic_match = []
    keyword1 = []
    for param1 in req_par1:
        # Check each keyword contained in each list of requested_parameters_1
        for keyword in param1:
            # If the keyword is contained in the text return all topics that have that keyword as first parameter
            if keyword in text:
                if keyword not in keyword1:
                    keyword1.append(keyword)
                topics1 = [i for i, x in enumerate(req_par1) if x == param1] #not sure of this fucking line
                for t in topics1:
                    if t not in param1_topic_match:
                        param1_topic_match.append(t)

    # If no keyword 1 is found - do not change topic
    if not keyword1:
        print("No keyword 1 found - return topic ", -1)
        return -1

    # print("\nSecond parameters of those topics: ")
    matching_topic_numbers = []
    keyword2 = []
    for n_topic in range(tot_topic):
        if n_topic in param1_topic_match:
            # print(n_topic)
            # print(req_par2[n_topic])
            for keyword in req_par2[n_topic]:
                if keyword in text or keyword == "*":
                    if keyword not in keyword2:
                        keyword2.append(keyword)
                    if n_topic not in matching_topic_numbers:
                        matching_topic_numbers.append(n_topic)

    # If no keyword 2 is found - do not change topic
    if not keyword2:
        print("No keyword 2 found - return topic ", -1)
        return -1

    matching_topics = []
    for n_topic in matching_topic_numbers:
        matching_topics.append(id_req[n_topic])

    print("Matching topics: ", matching_topic_numbers)
    # When the function is called from here it means we are processing the user sentence, hence we allow to return
    # topics with likeliness zero, if there are no topics with likeliness different from zero.
    nxt_topic = choose_topic(matching_topic_numbers, likelinesses, True)
    return nxt_topic


if __name__ == '__main__':
     #Open the json file containing the keywords
    base_id_req, base_topics_likeliness, base_req_par1, base_req_par2, base_tot_topic = \
        get_topics_keywords_and_likelinesses()
    main(sys.argv[1], base_id_req, base_topics_likeliness, base_req_par1, base_req_par2, base_tot_topic)
