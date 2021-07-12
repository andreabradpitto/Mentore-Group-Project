from topics_utils import get_topics_sentences
sentence_type =[]
school_topics_sentences_types, school_topics_sentences = get_topics_sentences()
for i in range(len(school_topics_sentences_types)):
               sentence_type.append(school_topics_sentences_types[i])
##
dict={}
for idx, school_topics in enumerate(school_topics_sentences_types):
    dict[idx] = school_topics[0:]

idxlist = []
for idx, school_topics in enumerate(school_topics_sentences_types):
     dict[idx]  = [school_topics[0:]]

questions1 = {}

for idx, school_topics in enumerate(school_topics_sentences_types):
    questions1[idx] = school_topics[0:]
#print(questions1)
   

questions2 = {}
for idx, school_sentences in enumerate(school_topics_sentences):
    questions2[idx] = school_sentences[0:]
#print(questions2)


#school_topics = [0, 2, 4]
#questions1 = {2: ['c', 'c', 'r', 'r', 'r', 'r', 'r', 'r'], 
#             4: ['c', 'c',
#             
#              'c', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']}
#questions2 = {2: ['What is the analysis of random phenomena?', 'What is the probability??', 'Factorial?2_w', 'Probability is a branch of Geography?1_w', 'Logarithm?2_w', 'Probabillity is a branch of History?1_w', 'Probabillity is a branch of Mathematics?1_c', 'Probabillity?2_c'],
#              4: ['What is the hotest continent in the Earth??', 'How many continents exist in the world??', 'What is the second largest continent in the Earth??', 'America?3_w', 'Europe?3_w', 'eight?2_w', 'America?1_w', 'Europe?1_w', 'Six?2_c', 'five?2_w', 'seven?2_w', 'Antarctica?1_w', 'Antarctica?3_w', 'Africa?3_c', 'Australia?1_w', 'Africa?1_c', 'Australia?3_w']
#}

print("Welcome to this fun quiz! \nAre you ready to test your knowledge?")
input("Press any key to start the fun ;) ")



for i in questions2:
    answerlist = questions2[i]
    quest = []
    print(answerlist)
    
    for value in range(len(questions2[i])):

        if questions1[i][value] == 'c':

            print(questions2[i][value])
            #Here we are storing the index of the question in the in the variable to test 
            iidd = answerlist.index(questions2[i][value])
            answer = input("type the answer:")

            for idx, x in enumerate(answerlist):
                r_or_c = questions1[i]
                splitting_answer = answerlist[idx].split("?")
                splitting_answer_correct = answerlist[idx].split("?")[0].split(".")
                if answer != splitting_answer[0] and r_or_c[idx] == "r":
                    print("Wrong Answer")
                    break

                if answer == splitting_answer[0] and r_or_c[idx] == "r":

                    if splitting_answer_correct[1] == "c" and str(iidd+1) == splitting_answer_correct[0]:
                        print("correct Answer")
                        break
                    if (splitting_answer_correct[1] == "c" and str(iidd+1) != splitting_answer_correct[0]) or splitting_answer_correct[1] == "w":
                        print("Wrong Answer")
                        break
      



print("Thanks for playing!")




