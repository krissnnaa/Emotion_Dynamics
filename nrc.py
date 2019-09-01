import csv
from nltk.tokenize import RegexpTokenizer
import influxdb
import re
from datetime import datetime
from nltk.corpus import stopwords
import sys
import os

name = sys.argv[1]
measurementName = sys.argv[2]
print(name, '\t', measurementName)
stop_words = set(stopwords.words('english'))
dirPath = os.getcwd()
dataDict = {}
with open(name + '.csv', encoding='UTF-8') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=";")
    check = 0
    for row in dataReader:
        if check != 0:
            dataDict[int(row[0])] = row[2]
        check = 1

angerDict = {}
with open(name + '_prediction_anger.csv', encoding='UTF-8') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=",")
    check = 0
    for row in dataReader:
        if check != 0:
            if row[1] == 'YES':
                angerDict[int(row[0])] = dataDict[int(row[0])]
        check = 1

fearDict = {}
with open(name + '_prediction_fear.csv', encoding='UTF-8') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=",")
    check = 0
    for row in dataReader:
        if check != 0:
            if row[1] == 'YES':
                fearDict[int(row[0])] = dataDict[int(row[0])]
        check = 1

joyDict = {}
with open(name + '_prediction_joy.csv', encoding='UTF-8') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=",")
    check = 0
    for row in dataReader:
        if check != 0:
            if row[1] == 'YES':
                joyDict[int(row[0])] = dataDict[int(row[0])]
        check = 1

sadDict = {}
with open(name + '_prediction_sadness.csv', encoding='UTF-8') as csvfile:
    dataReader = csv.reader(csvfile, delimiter=",")
    check = 0
    for row in dataReader:
        if check != 0:
            if row[1] == 'YES':
                sadDict[int(row[0])] = dataDict[int(row[0])]
        check = 1

with open(dirPath + '/nrcValue/' + 'nrcEmotion.txt', 'r') as f:
    fileRead = [x.strip('\n') for x in f.readlines()]
    data = [x.split('\t') for x in fileRead[1:]]

emoAnger = {}
emoFear = {}
emoJoy = {}
emoSad = {}

for item in data:
    if item[2] == 'anger':
        emoAnger[item[0]] = item[1]
    elif item[2] == 'fear':
        emoFear[item[0]] = item[1]
    elif item[2] == 'joy':
        emoJoy[item[0]] = item[1]
    else:
        emoSad[item[0]] = item[1]

angerEmo = {}
fearEmo = {}
joyEmo = {}
sadEmo = {}

for key in dataDict.keys():
    angerEmo[key] = 0
    fearEmo[key] = 0
    joyEmo[key] = 0
    sadEmo[key] = 0

for key, text in angerDict.items():
    angerSum = 0
    tokenizer = RegexpTokenizer(r'\w+')
    textTokenize = tokenizer.tokenize(text)
    afterStopWords = [w for w in textTokenize if not w in stop_words]
    for word, emoValue in emoAnger.items():
        if word in afterStopWords:
            angerSum = angerSum + float(emoValue)
    avgValue = angerSum / len(textTokenize)
    angerEmo[key] = avgValue

for key, text in fearDict.items():
    fearSum = 0
    tokenizer = RegexpTokenizer(r'\w+')
    textTokenize = tokenizer.tokenize(text)
    afterStopWords = [w for w in textTokenize if not w in stop_words]
    for word, emoValue in emoFear.items():
        if word in afterStopWords:
            fearSum = fearSum + float(emoValue)
    avgValue = fearSum / len(textTokenize)
    fearEmo[key] = avgValue

for key, text in joyDict.items():
    joySum = 0
    tokenizer = RegexpTokenizer(r'\w+')
    textTokenize = tokenizer.tokenize(text)
    afterStopWords = [w for w in textTokenize if not w in stop_words]
    for word, emoValue in emoJoy.items():
        if word in afterStopWords:
            joySum = joySum + float(emoValue)
    avgValue = joySum / len(textTokenize)
    joyEmo[key] = avgValue

for key, text in sadDict.items():
    sadSum = 0
    tokenizer = RegexpTokenizer(r'\w+')
    textTokenize = tokenizer.tokenize(text)
    afterStopWords = [w for w in textTokenize if not w in stop_words]
    for word, emoValue in emoSad.items():
        if word in afterStopWords:
            sadSum = sadSum + float(emoValue)
    avgValue = sadSum / len(textTokenize)
    sadEmo[key] = avgValue

angerFile = []
for key, value in angerEmo.items():
    angerFile.append(value)

fearFile = []
for key, value in fearEmo.items():
    fearFile.append(value)

joyFile = []
for key, value in joyEmo.items():
    joyFile.append(value)

sadFile = []
for key, value in sadEmo.items():
    sadFile.append(value)

with open(name + '_data.txt', 'r', encoding='utf-8') as fd:
    dataFile = [l.strip().split('\t\t')[1:] for l in fd.readlines()][1:]

finalJson = []
for item, anger, joy, fear, sad in zip(dataFile, angerFile, joyFile, fearFile, sadFile):
    createDate = re.findall(r'\d{4}-\d{2}-\d{2}', item[0])
    createDate = ''.join(createDate)
    dateForm = datetime.strptime(createDate, '%Y-%m-%d')
    ang = float(anger)
    joy = float(joy)
    fear = float(fear)
    sad = float(sad)
    msgDict = {}
    angDict = {}
    joyDict = {}
    fearDict = {}
    sadDict = {}
    fieldDict = {}
    user = {}
    dataDict = {}
    msgDict['Comments'] = item[1]
    angDict['Anger'] = ang
    joyDict['Joy'] = joy
    fearDict['Fear'] = fear
    sadDict['Sadness'] = sad
    fieldDict.update(msgDict)
    fieldDict.update(angDict)
    fieldDict.update(joyDict)
    fieldDict.update(fearDict)
    fieldDict.update(sadDict)
    if name.startswith('other'):
        user['Participant'] = name.split("_")[1]
        user['Participant association'] = 'Other'
    else:
        user['Participant'] = name
        user['Participant association'] = 'Member'
    dataDict['tags'] = user
    dataDict['fields'] = fieldDict
    dataDict['time'] = dateForm
    dataDict['measurement'] = measurementName
    finalJson.append(dataDict)

client = influxdb.InfluxDBClient(host='localhost', port=8086)
client.switch_database('emotionDatabase')
client.write_points(finalJson)

print("Done!!!")
