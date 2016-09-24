
# coding: utf-8

#### import ####
from __future__ import division

from math import log

import utils

#------ Utils functions ------#
def extract_tokens(title):
    return set(title.split(" "))


def process_file(file_name):
    with open(file_name,'r') as f :
        titles = f.readlines()
    return map(lambda e : extract_tokens(e.replace("\n","")),titles)


def count_occurrence(token,pop):
    count = 0
    for tokens in pop :
        if token in tokens :
            count +=1
    return count


def propX(X,Y):
    return X/(X+Y)


def entropy(cA,cB):
    pA = propX(cA,cB)
    pB = propX(cB,cA)
    return -log(pA**pA,2) -log(pB**pB,2)   #log(a**a) notation to avoid log of zero


## Compute the information gain for a given token
def information_gain(token,popA,popB):
    # First we count the occurence of the token in the class A and B
    countA = count_occurrence(token,popA)
    countB = count_occurrence(token,popB)

    # Then we can compute the entropy related to subset containg the token and subset which do not.
    entropy_token = entropy(countA,countB)
    entropy_not_token = entropy(len(popA)-countA,len(popB)-countB)
    p_t = (countA+countB)/(len(popA)+len(popB))

    # After that we can compute the estimated entropy generated by the split by averaging
    # by the probability of having the token (or not) in the entire population
    estimated_entropy = p_t*entropy_token + (1-p_t)*entropy_not_token

    # Eventually we return the information gain
    return entropy(len(popA),len(popB)) - estimated_entropy
# TODO : compute the entropy of the class before or after but not for every token...


def compute_gain(a,b):
    # Gather all the tokens in one set
    tokens = set()
    for token_set in a+b:
        tokens.update(token_set)
    # compute and sort by gain
    token_information = sorted(
        [(token,information_gain(token,a,b)) for token in tokens],
        key = lambda x : x[1],
        reverse=True)
    return token_information


def main():

    #------ File and data processing ------#
    output_file = "results.txt"
    title_file_A = "titles_A.txt"
    title_file_B = "titles_B.txt"

    class_A = process_file(title_file_A)
    class_B = process_file(title_file_B)

    #------ Compute and Sort information gain ------#
    token_information = compute_gain(class_A,class_B)
    sorted_tokens = map(lambda e : e[0],token_information)

    #------ Print and save top 100 tokens ------#
    utils.save_in_file(output_file, sorted_tokens[:100])
    for e  in token_information[:100]:
        print(e)

if __name__ == '__main__':
    main()
