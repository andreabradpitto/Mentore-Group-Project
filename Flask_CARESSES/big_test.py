import os

string = ""
for i in range(100):
    string = string + "python test_dialogue_manager.py " + str(i)
    if i < 100:
        string = string + " & "

os.system(string)
