#!/usr/bin/python

import os
import fileinput
import re
import json

speech = ""
dialogue = {}

#speech-to-text api
#stores output in output.txt
os.system('curl -X POST -u cd6bc024-34f1-4c10-9495-aa893591a578:WEp4daKfsyeI --header "Content-Type: audio/flac" --data-binary @ted_talk.flac "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize" > output.txt')
with open('output.txt', 'r') as f:
    for line in f:
        #get transcript from output.txt
        if re.search('transcript', line):
            line = line.strip()
            line = line[15:-1]
            speech += line

#need dict to create json file
dialogue["text"] = speech
#need json file to use tone analyzer
with open('result.json', 'w') as f:
    json.dump(dialogue, f)

#tone analyzer stores output in output2.txt
os.system('curl -X POST -u "2a95ca1d-a29f-40e5-b37b-9a2b1ac4e5fa":"TYAYjJOlfAie" --header "Content-Type: application/json" --data-binary @result.json "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19&tones=emotion" > output2.txt')

string = "" #string to hold tone analyzer output
tone_scores = {} #to hold tones and their respective scores

#read output2.txt into a string so we can parse
with open('output2.txt', 'r') as f:
    for line in f:
        string = string + line

#check for any emotions detected
if '\"tones\"' in string:
    tones_remaining = True

#create dict of tone scores
while tones_remaining:
    index_score = string.find('score')
    index_toneid = string.find('tone_id')
    index_tonename = string.find('tone_name')

    score = string[index_score+7:index_toneid-2]
    score = float(score)
    tone_id = string[index_toneid+10:index_tonename-3]

    tone_scores[tone_id] = score

    string = string[(index_tonename+len(tone_id)):]
    if string.find('score') == -1:
        tones_remaining = False

 ###################
 # Output + Results
 ###################

print "\nThe audio used is a 45 second segment from a TED talk"
print "Transcript: \n%s" %(speech)

print "\nAll emotion tone scores: "
print tone_scores

print "\nOutput to user:"

if tone_scores['anger'] > 0.1:
    print "After analyzing the dialogue in the workplace, it seems like your workers are feeling angry."
if tone_scores['fear'] > 0.1:
    print "After analyzing the dialogue in the workplace, it seems like your workers are feeling scared."
if tone_scores['sadness'] > 0.1:
    print "After analyzing the dialogue in the workplace, it seems like your workers are feeling sad."
if tone_scores['disgust'] > 0.1:
    print "After analyzing the dialogue in the workplace, it seems like your workers are feeling disgusted."
