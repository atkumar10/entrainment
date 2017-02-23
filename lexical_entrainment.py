'''
@author: Anish, Zahra
group lexical entrainment
measure (weighted team average) 
implementation of heather's formulsa
'''
import textProcessingUtil as util
import sys
import pandas as pd

def get_teamID(index):
        if len(index.split('_')) == 1 and len(index.split('-')) < 2:
            return index
        elif index[0]=='T':
            index.split('_')[1]
        else:
            return index[0:4]
def get_playerID(index):
    if index[0]=='T':
        return index.split('_')[-1].split('-')[-1]
    else:
        return index[-1]
def read_word_pergame_file(filePath):
        word_game_dic = {}
        input_file = open(filePath, 'r')
        print('Reading file\n')
        lines = input_file.readlines()
        input_file.close()
        i=0
        for line in lines:
            if i == 0:
                teamID = line
                word_game_dic[teamID]=[]
                i+=1
            elif line == '':
                i=0
            else:
                word_game_dic[teamID].append(line)  
                i+=1
        return word_game_dic

def read_aggregate_frequency_file(csvFile):
    return pd.read_csv(csvFile,index_col = 0)
    
        
        
        
def Baseline(bow,word_game_dic):

        #output_file = open('lexicalentrain'+ file_name[4:8] + file_name[-17:-12]+ '.txt', 'w')

        #Open input filed and read the input into variable
        
        print('Analyzing file', file_name[:4], file_name[4:8], file_name[-17:-12], '\n')

       # processed_lines = util.overallprocess(lines)
        
        #dictionary with key: tuple with (player number, word), value: number of times given player
        #has uttered given word
        player_dict = get_player_dict(processed_lines)
        #dictionary with key: speaker id, value: total number of words uttered 
        total_player_counts = get_total_player_counts(processed_lines)


        for index , row in bow.iteritems():
            teamID = get_teamID(index)
            player = get_playerID(index)
            words = word_game_dic[teamID]
            for index2 , row2 in bow.iteritems():
                teamID2 = get_teamID(index2)
                player2 = get_playerID(index2)
                
                if (teamID == teamID2) and (player < player2):
                    dyad[(index,index2)] =  -1 * abs(bow[index][words]/bow[index]['#total'] - bow[index2][words]/bow[index2]['#total'])
                    w = (bow[index]['#total']+bow[index2]['#total'])
                    weighted_dyad[(index,index2)] = w * dyad[(index,index2)]
                    sum_total_dyads += w
                    weighted_team[teamID] += weighted_dyad[(index,index2)]
        
        
        
        
        weighted_team[teamID]
        
        player = 1
        match = 2
        dyad_entrainment_list = []
        #Iterate through each dyad pair
        print('Calculating dyad entrainment measures\n')
        while (player < len(total_player_counts)+1):
                while (player < match and match < len(total_player_counts)+1):

                        #Calculate the dyad entrainment measures for each of the following words
                        for word in ['i']:

                                #Compute the difference in absolute use of certain words between each player dyad
                                dyad_diff = (player, player_dict[(player, word)], match, (player_dict[(match, word)]))

                                #Compute the similarity measure for the dyad
                                dyad_measure = (dyad_entrainment(dyad_diff, total_player_counts))

                                #Add dyad measures to list for group entrainment measure calculation
                                dyad_entrainment_list.append(dyad_entrainment(dyad_diff, total_player_counts))

                                output_file.write(' '.join([str(player), str(match), str(dyad_measure[2])]))
                                output_file.write('\n')
                                
                        match = match +1
                player = player +1
                match = player +1


        #Calculate and print the weighted average entrainment measure for all dyad pairs in group
        print('Calculating group entrainment measure\n')
        group_measure = group_entrainment(dyad_entrainment_list, total_player_counts)
        output_file.write(' '.join(['Group', str(group_measure)]))

        output_file.close()



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


def dyad_entrainment(dyad_diff, player_total):
    #calculate the measure of entrainment for a dyad based on a certain word
    prop1= dyad_diff[1]/player_total[dyad_diff[0]]
    prop2= dyad_diff[3]/player_total[dyad_diff[2]]
    return (dyad_diff[0], dyad_diff[2], -1 * abs((prop1-prop2)))

def group_entrainment (dyad, player_total):
    #calculate a weighted average of the individual dyad measures
    num = []
    denom = []
    for entry in dyad: 
        num.append((abs(entry[2]) * (player_total[entry[0]] + player_total[entry[1]])))
        denom.append(player_total[entry[0]] + player_total[entry[1]])
    return ((-1* sum(num))/sum(denom))

if __name__=="__main__":
    main(sys.argv[1])
        
    





