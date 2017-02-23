"""
@author: Anish
Processes transcripts and extracts feature values for lexical proximity measures
Input: All game transcripts; lexical items to measure for proximity
Output: CSV file with feature values (number of utterances per speaker per word
and total number of utterances per speaker) 
"""

from nltk.stem import PorterStemmer
import pickle
import glob
import pandas
import textProcessingUtil as util
ps = PorterStemmer()


def get_player_dict(processed_lines):
    player_dict = {}
    for sent in processed_lines:
        for word in sent[1]:
            #if speaker and word pair tuple is in dictionary, incremement value by 1
            if (sent[0], word) in player_dict:
                player_dict[(sent[0], word)]=player_dict[(sent[0], word)]+1
            #if speaker and word pair tuple is not in dictionary, add it with value 1
            else:
                player_dict[(sent[0], word)]= 1
    return player_dict

def get_total_player_counts(processed_lines):
    #Dictionary for speaker counts, key: speaker number, number of words uttered by speaker
    total = {}
    for sent in processed_lines:
        #iterate through every utterance for given speaker and increment for every word uttered
        for word in sent[1]:
            if sent[0] in total:
                total[sent[0]] = total[sent[0]] + 1
            else:
                total[sent[0]] = 1

    return total

#df = pandas.read_csv('/Users/atkumar10/Documents/Litman Lab/transcriptions/Game1_transcripts/full_topic_sigs_unverified/game_top_words.csv')
#word_iter = df.iterrows()
#while next(word_iter)
#prepare input files: all segment transcriptions 
files = glob.glob('/Volumes/litman/Transcriptions/Game1_text_transcripts/half_verified/Standardized/Text/*.txt')

speaker_id = []
word_tokens = []
total_tokens =[]



#load dict with top topic words for each game (key is game number, value is list of top words)
r = open('/Volumes/litman/Transcriptions/Python/Lexical Entrainment/output/top_25_topic_sigs', 'rb')
game_words = pickle.load(r)
r.close()

#LDA_topics = 

#LDA_topics = set(w.strip() for w in LDA_topics.split(','))

word_list = [ps.stem(w) for w in game_words]
    
dfdict = {}          
for file in files:
        input_file = open(file, 'r')
        processed_lines = util.overallprocess(input_file.readlines())
        input_file.close()      

        team_num = file[file.find('Team')+4 : file.find('Team')+8]
        game_num = file[file.find('Game', 86, -1):file.find('Game', 86, -1)+5]
        
        #dictionary with key: tuple with (player number, word), value: number of times given player
        #has uttered given word
        player_dict = get_player_dict(processed_lines)

        #dictionary with key: speaker id, value: total number of words uttered 
        total_player_counts = get_total_player_counts(processed_lines)

        #word_list = [ps.stem(w) for w in ['and', 'with', 'but', 'chalices']

        for player in range(len(total_player_counts)):
            speaker_id = team_num + ' ' + game_num + '-' + str(player+1)
            dfdict[speaker_id] = {}

            for word in word_list:

                try:
                    player_word_count = player_dict[(player+1, word)]
                except KeyError:
                    player_word_count = 0
                    
                dfdict[speaker_id][word]=(player_word_count)

            try:
                player_total = total_player_counts[player+1]
            except KeyError:
                player_total = 0
                
            dfdict[speaker_id]['total']=(player_total)


df = pandas.DataFrame.from_dict(dfdict,orient='index')
df.to_csv('/Volumes/litman/Transcriptions/Game1_text_transcripts/half_verified/Features/game1_features_top25_topic_sigs.csv')

            
