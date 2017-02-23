"""
@author: Anish
Computes tf-idf measures for each transcript
"""

import glob, os, sys, math, pickle, pandas
from nltk.stem import PorterStemmer
print ('working')

ps = PorterStemmer()
sys.path.append('/Volumes/litman/Transcriptions/Python/Lexical Entrainment/src')

import textProcessingUtil as util

os.chdir('/Volumes/litman/Transcriptions/Game1_text_transcripts/half_verified/Standardized/Text/')

files = glob.glob('*standardized.txt')


newlines = []
counter = 1
word_dict = {}

fillers = ['laughs', 'ta', 'tss', 'um', 'hmm', 'mmm', 'mm', 'hm',
           'tsss', 'tt', 'ttt', 'opp', 'op','ah', 'ahh', 'uh', 'uhh',
           'mmhmm', 'ha', 'ooo', 'oo', 'mhmm', 'ch', 'mhm', 'mmk','em','eh',
           'mk', 'mmk', 'ttt', 'tt', 'umm', 'em', 'ee', 'hmmm', 'nnmm',
           'nnmhh', 'ehhh' ]

for file in files:
    file_dict = {}
    with open(file, 'r') as t:
        lines = t.readlines()
        for line in lines:
            newline = line[4:]
            newline = util.preprocess(newline)
            newline = util.tokenize(newline)
            newline = [ps.stem(w) for w in newline]
            for word in newline:
                if word in file_dict:
                    file_dict[word] += 1
                else:
                    file_dict[word] = 1
            newlines.append(newline)
        word_dict[file[4:8]] = file_dict


r = open('corpus', 'wb')
pickle.dump(word_dict, r)
r.close()

def idf(word):
    counter = 0
    for file in word_dict:
        if word in word_dict[file]:
            counter += 1
    #print ('counter:', counter, 'len:', len(word_dict))
    if counter == 0:
        return 0
    else: 
        return math.log(len(word_dict)/counter)

def total_doc_words(file):
    total_words = 0
    for word in word_dict[file]:
        total_words+=word_dict[file][word]
    return total_words

def tf(word, file):
    counter = 0
    total_words = total_doc_words(file)
    try:
        counter = word_dict[file][word]
    except KeyError:
        counter = 0
    #for file in word_dict:
        #if word in word_dict[file]:
            #counter += word_dict[file][word]
    return (counter / total_words)

def tf_idf(word, file):
    return tf(word, file) * idf(word)

#file = files[0]
print(len(files))
all_measures = {}
for file in files:
    with open(file, 'r') as t:
        team_measures = {}
        lines = t.readlines()
        for line in lines:
            newline = line[4:]
            newline = util.preprocess(newline)
            newline = util.tokenize(newline)
            newline = [ps.stem(w) for w in newline]
            for word in newline:
                measure = tf_idf(word, file[4:8])
                if word not in team_measures: 
                    #team_measures[word] = tf_idf(word, file[4:8])
                    team_measures[word] = (measure, tf(word,file[4:8]))
        all_measures[file[4:8]] = team_measures

allterms = []

r = open('/Volumes/litman/Transcriptions/Python/Lexical Entrainment/output/top20list.txt', 'w')
for file in all_measures:
    print(file)
    r.write(file+'\n')
    terms = sorted(all_measures[file].items(), key = lambda x: x[1], reverse = True)
    terms = [w for w in terms if w[0] not in fillers][:20]
    for w in terms:
        allterms.append(w)
        r.write(str(w[0]) + ' idf: ' + str(w[1][0]) + ' tf: ' + str(w[1][1]) +'\n')
        print (w)
    print ('\n')
    r.write('\n')
r.close()

os.chdir('/Volumes/litman/Transcriptions/Python/Lexical Entrainment/output')
r = open('tfidif_top20_per_game', 'wb')
pickle.dump(allterms, r)
r.close()
                   
            


