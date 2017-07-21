#!/usr/bin/python

import os
import sys
import fileinput
import re
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3



#hard coded for speech to text
userID = "f427c1c3-4e22-4f67-94b5-57d8273eb54d"
pw = "XJNCxHwKhsse"

#speech-to-text api
#stores output in output.txt
cmd = 'curl -X POST -u %s:%s --header "Content-Type: audio/flac" --data-binary @ted_talk.flac "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize" > output.txt' %(userID, pw)
os.system(cmd)

speech = ""
dialogue = {}

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

#hard coded for tone analyzer
userID = "0382dac1-a3a5-476f-8530-f58e91308246"
pw = "uo8bAFazuZdo"

#tone analyzer api
#stores output in output2.txt
cmd = 'curl -X POST -u "%s":"%s" --header "Content-Type: application/json" --data-binary @result.json "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19&tones=emotion" > output2.txt' %(userID, pw)
os.system(cmd)

string = "" #string to hold tone analyzer output
tone_scores = {} #to hold tones and their respective scores
tones_remaining = False

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

### Visual recognition

api_key = "fe6e0c5999c4c280402051d2e6e1ec5d88a9a30f"
classifier_id='People_1425066267'
visual_recognition = VisualRecognitionV3('2016-05-20', api_key=api_key)

happy_path = join(dirname(__file__), 'happy.jpg')

with open(happy_path, 'rb') as images_file:
    data = visual_recognition.classify(images_file=images_file, classifier_ids=[classifier_id], threshold=0)
    json_str = json.dumps(data)

resp = json.loads(json_str)

print(resp)

# Parse visual recognition later

# string2 = "" #string to hold visual analyzer output
# visual_scores = {} #to hold visual classes and their respective scores
# class_remaining = False
#
# visual_scores['Happy'] = 0
# visual_scores['Nothappy'] = 0
# visual_scores['Negative'] = 0
#
# #read output2.txt into a string so we can parse
# with open('output3.txt', 'r') as f:
#     for line in f:
#         string2 = string2 + line
#
# print string2 #for debug
#
# #check for any emotions detected
# if 'images' in string2:
#     class_remaining = True
#
# #create dict of tone scores
# while class_remaining:
#     index_score = string.find('score')
#     score = string[index_score+8:index_score+15]
#     score = float(score)
#     print score
#
#     if visual_scores['Happy'] == 0:
#         visual_scores['Happy'] = score
#     elif visual_scores['Nothappy'] == 0:
#         visual_scores['Nothappy'] = score
#     else:
#         visual_scores['Negative'] = score
#
#     string2 = string2[index_score+15:]
#     if string2.find('score') == -1:
#         class_remaining = False
#
# print visual_scores
