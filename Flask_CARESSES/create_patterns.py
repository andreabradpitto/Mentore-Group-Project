import pickle
import random

patterns = [['q']]

with open("dialogue_tree/patterns.txt", 'wb') as f:
    pickle.dump(patterns, f)

# Test the patterns that have been written on the file
with open("dialogue_tree/patterns.txt", 'rb') as f:
    patterns = pickle.load(f)

print(random.choice(patterns))
