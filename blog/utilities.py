import os
import pathlib

module_path = pathlib.Path(__file__)
common_filename = module_path.parent.joinpath("common.txt")

common_file = open(common_filename, "r")

a = common_file.readlines() #"\n"
common_list = []


for word in a:
    word = word.replace("\n", "")
    common_list.append(word)


# how to handle numbers and special characters?
# how to handle repeated words?
# how to handle important but too frequent words?
# how to handle empty list after removing too frequent words?
### https://de.wikipedia.org/wiki/Tf-idf-Ma%C3%9F
def key_word_finder(text):
    text = text.lower()
    text = text.split()
    keep_text = []
    
    for word in text:
        # NOTE: tmp solution!!!
        if word not in common_list and len(keep_text) <= 20: 
            keep_text.append(word)


    return keep_text
print(key_word_finder("The best of and a Tim Franck"))