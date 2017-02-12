##Script to extract speaker data in format to prepare for entrainment measures
##Input file: Higgins XML annotation file
##Output files: (1) text file with speaker id, :, and utterance
##              (2) text file with speaker id, :, lexical item 

import xml.etree.ElementTree as ET
import sys

def main(args):
    #print (args)
    
    output_seg = args[1].replace(".xml","_segment.txt")
    #output_word = args[1].replace(".xml","_word.txt")
    #print (output_seg)
    #print (output_word)

    raw = ET.parse(args[1])
    #print (raw)
    root = raw.getroot()
    #print (root)

    #extracts all tokens from each participant and puts them into one list; iter searches for the '/t' tag
    allwords = []
    roottag = '{http://www.speech.kth.se/higgins/2005/annotation/}t'
    for t in root.getchildren()[1].iter(roottag):
        allwords.append(t.text)

    #extracts a list of individual segments
    allsegments = root.getchildren()[1].getchildren()

    #extracts each utterance as a string and adds to a list with speaker number and utterance
    utter = []
    for segment in allsegments:
        for transcription in segment.getchildren():
            newseg = ''
            for t in transcription.getchildren():
                if t.tag == '{http://www.speech.kth.se/higgins/2005/annotation/}t':
                    newseg = newseg + ' ' + str(t.text)
            if len(newseg)>0:
                utter.append(segment.attrib['track'][5] + ' : ' + newseg.lstrip() + '\n')

    #extracts each lexical entry and adds to a list with speaker number 
    lexical = []
    for segment in allsegments:
        for transcription in segment.getchildren():
            for t in transcription.getchildren():
                if t.tag == '{http://www.speech.kth.se/higgins/2005/annotation/}t':
                    lexical.append(segment.attrib['track'][5] + ' : ' + t.text + '\n')

    seg = open(output_seg, 'w')
    #word = open(output_word,'w')

    seg.writelines(utter)
    seg.close()
    print('success for', args[1], '\n')
    #word.writelines(lexical)
    #word.close()


if __name__ == "__main__":
    
    main(sys.argv)
    

