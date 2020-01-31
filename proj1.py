#!/usr/bin/env python
# coding: utf-8

# In[17]:


"""Karuna Gujar
    CSCI 6350-001
    Project #1
    Due: 01/30/2020
    
    Project: This project implements the minimum edit distance algorithm and backtracks to output edit operations. The minimum distance is calculated using both Levenshtein costs and Confusion matrix (given) with a goal to perform analysis and comparitive study between two costs.
"""

import numpy as np
import sys
import random
import csv
import pandas as pd

string_src = ''
string_trg = ''

len_src=len(string_src)
len_trg=len(string_trg)
rows = len_src +1
cols = len_trg +1

del_cost = 1
inst_cost = 1

"""function to read the csv file into dictionary. 
For eg: {'ak':'3', 'al':'1'}
"""
def readCsvToDict(csvFile):
    costDict = {}
    data = pd.read_csv(csvFile, header=None)
    mat = data.values
    for i in range(1,len(mat)):
        src = mat[i][0]
        for j in range(1,len(mat[i])):
            trg = mat[0][j]
            cost = mat[i][j]
            costDict[src+trg] = cost
    return costDict


"""Fuction which reads the words tesxt file and processes a pair of source-target words one at a time.

"""
def readWordsAndProcess(textFile):
    with open('words.txt','r') as f:
        for line in f:
            words = line.split()
            target_word = words[0]
            for i in range(1,len(words)):
                src_word = words[i]
                find_minumum_distance(src_word, target_word)
                print("--------------------------------------------------\n\n")
                
    
"""function which generates allignment matrix to preserve the direction of the minimum distance.
'u' is for up, 'd' is for diagnol, 'l' is for left, 'a' is for all there directions.
paris of the above directions, like 'ul', 'du', 'dl' is also possible.
"""
def findAllignment(diag, up, lt):
   
    if (diag < up) and (diag < lt):
        allign = 'd'
    elif (up < diag) and (up < lt):
        allign = 'u'
    elif (lt < diag) and (lt < up):
        allign = 'l'
    elif (lt == up) and (lt < diag):
        allign = 'ul'
    elif (diag == up) and (diag < lt):
        allign = 'du'
    elif (diag == lt) and (diag < up):
        allign = 'dl'
    else:
        allign = 'a'
 
    return allign

"""function which calculates the minimum distance 
given the costMatrix for susbcstituion and costs for deletion ad insertion.
""" 
def min_distance(distance, a, costDict):
    for i in range(1,rows):
        for j in range(1,cols):
            str1 = string_src[i-1]+string_trg[j-1]
            sub_cost = costDict.get(str1)
            if string_src[i-1] == string_trg[j-1]:
                diag = distance[i-1,j-1] + 0
            else:
                diag = distance[i-1,j-1] + int(sub_cost)
            up = distance[i-1,j] + del_cost
            left = distance[i,j-1] + inst_cost
            a[i][j] = findAllignment(diag, up, left)
            distance[i,j] = min(diag,left,up)
    return distance, a

"""function performs the backtracking. Depending on the allignment the source and targewt strings are modified.
"""
def backtracking(allignmnt, distance):
    i = len_src-1
    j = len_trg-1
    ptr_i = rows-1
    ptr_j = cols-1
    
    str_pipes = ''
    str_op = ''   
    output_src = ''
    output_trg = ''
    
    while i>=0 or j>=0 :
        str_pipes = '| ' + str_pipes
        allignment = allignmnt[ptr_i][ptr_j]
        
        if allignment == 'ul': choice = random.choice(['u','l'])
        elif allignment == 'dl': choice = random.choice(['d','l'])
        elif allignment == 'du': choice = random.choice(['d','u'])
        elif allignment == 'a' : choice = random.choice(['d','l','u'])
        else: choice = allignment
        if choice == 'u': 
            output_src = string_src[i]+ ' ' + output_src
            i = i -1
            output_trg = '* ' + output_trg
            ptr_i=ptr_i -1
            str_op = 'd ' + str_op
        elif choice == 'l':
            output_src = '* ' + output_src
            output_trg = string_trg[j] + ' ' + output_trg
            j = j-1
            ptr_j = ptr_j-1
            str_op = 'i ' + str_op
        elif choice == 'd':
            output_src = string_src[i] + ' ' + output_src
            output_trg = string_trg[j] + ' ' + output_trg
            if(string_src[i] == string_trg[j]):       
                str_op = 'k ' + str_op
            elif (string_src[i] != string_trg[j]):
                str_op = 's ' + str_op         
            i = i-1
            j =j-1
            ptr_i = ptr_i-1
            ptr_j = ptr_j-1
            
                         
    print (output_src)
    print(str_pipes)
    print(output_trg)
    print(str_op +'  (%s)' % distance[rows-1][cols-1])
        

"""This function contains the function calls to tother sub-functions.
"""
def find_minumum_distance(src, trg):        
    global string_src
    global string_trg
    global len_src
    global len_trg
    global rows
    global cols
    
    string_src = src
    string_trg = trg
    len_src=len(string_src)
    len_trg=len(string_trg)
    rows = len_src +1
    cols = len_trg +1
    
    confusionDict = readCsvToDict('costs2.csv')
    levenshteinDict = readCsvToDict('costs.csv')
      
    distance = np.zeros(shape=(rows,cols))
    allignment = [["" for x in range(cols)] for y in range(rows)]        

    for i in range(1, rows):
        distance[i][0] = i
        allignment[i][0] = 'u'

    for i in range(1, cols):
        distance[0][i] = i
        allignment[0][i] = 'l'
    
    min_distance(distance,allignment, levenshteinDict)
    backtracking(allignment, distance)
    print('\n')
    min_distance(distance,allignment, confusionDict)
    backtracking(allignment, distance)

readWordsAndProcess('words.txt')
#find_minumum_distance ('mischief','mischievious')
"""
a. Compare and contrast the results obtained from using the different cost approaches. Is one “better” than the other? How? Why?
Answer=> In most cases, the cost when confusion matrix was used is less than the cost when Levenshtein cost matrix was used. Using confusion matrix is better because it does not assume the costs for substitution as 2 but instead is based on statistical analysis of words.

b) While the algorithm you implemented yields the minimum edit distance between a pair of words, it is not clear how it fits into a larger context (e.g., where does it get the words from?). Provide a description of its plausible use in a natural language application context (how does one arrive at the candidate words, how is the correct spelling selected, etc.)
Answer => The practical application of edit distance could be a 1) spell checker   2) word suggestions as the user starts typing. Consider a scenario where we are looking for wrong spellings in a document and trying to correct it. We will read the entire document and see if every word is in the dictionary. If not, we find the word with minimum distance and can be corrected to the closest word. 

c) Explain how you might devise a new set of costs: what process would you go through? What data would you use or collect? How would you arrive at final values for the table?
Answer => I will get Wikipedia dataset and take top 50,000 words as the dictionary. Then I will substitute every letter of every word by every other letter and keep a count of valid substitutions. For e.g.: For word ‘Band’, when ‘b’ is replaced by ‘h’ it makes a valid substitution. Likewise I will count how many valid ‘b’ to ‘h’ substitutions are possible. This way I will create a matrix 26 X 26, take log of all the values , take inverse of these values.


"""


# In[ ]:





# In[ ]:




