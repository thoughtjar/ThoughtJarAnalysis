from flask import Flask, request, send_file, jsonify
import csv
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import collections
from textblob import TextBlob


application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"

@application.route("/csv", methods=['POST'])
def getCSV():
    data = json.loads(request.data)
    responseContent = data["responseContent"]
    f = csv.writer(open("data.csv", "w"))
    f.writerow(list(responseContent[0].keys()))
    for response in responseContent:
        row = []
        for key in responseContent[0].keys():
            row.append(response[key])
        f.writerow(row)
    with open('data.csv') as f:
        s = f.read() + '\n'
    return s

@application.route("/oneVarNum", methods=['POST'])
def oneVarNum():
    srcList = []
    data = json.loads(request.data)
    print(data)
    firstResponses = data["first"]
    firstQuestionResponses = []
    for stringNum in firstResponses:
        firstQuestionResponses.append(int(stringNum))
    print(firstQuestionResponses)
    print(type(firstQuestionResponses))
    s = pd.Series(firstQuestionResponses)
    fig = plt.figure()
    plot = sns.boxplot(x=s)
    plot.set(xlabel=data["firstQuestionField"])
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    src = base64.encodebytes(imgdata.getvalue()).decode()
    print(src)
    srcList.append(src)
    srcData = {"srcList": srcList}
    return jsonify(srcData)

@application.route("/oneVarMC", methods=['POST'])
def oneVarMC():
    srcList = []
    data = json.loads(request.data)
    print(data)
    fig = plt.figure()
    plot = sns.countplot(data["first"])
    plot.set(xlabel=data["firstQuestionField"], ylabel="frequency")
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    src = base64.encodebytes(imgdata.getvalue()).decode()
    print(src)
    srcList.append(src)
    srcData = {"srcList": srcList}
    return jsonify(srcData)

    '''
    #pandas piechart below
    hardcodedData = {'first': ['Brazil', 'Brazil', 'Brazil', 'Portugal', 'Germany', 'Germany', 'Argentina', 'Argentina', 'Brazil', 'Germany'], 'firstQuestionField': 'Who do you think will win the World Cup?'}
    responseFrequencyComplete = collections.Counter(hardcodedData['first'])
    responseFrequencyKeys = responseFrequencyComplete.keys()
    responseFrequencyValues = responseFrequencyComplete.values()

    pieChartDF = pd.DataFrame({'vals': responseFrequencyValues}, index = responseFrequencyKeys)
    pieChartVisual = pieChartDF.plot.pie(y='vals', figsize=(5, 5))
    #^^^^^^ that should be the image if the code works
    print(type(pieChartVisual))

    #matplotlib piechart
    hardcodedData = {'first': ['Brazil', 'Brazil', 'Brazil', 'Portugal', 'Germany', 'Germany', 'Argentina', 'Argentina', 'Brazil', 'Germany'], 'firstQuestionField': 'Who do you think will win the World Cup?'}
    responseFrequencyComplete = collections.Counter(hardcodedData['first'])
    responseFrequencyKeys = responseFrequencyComplete.keys()
    responseFrequencyValues = responseFrequencyComplete.values()

    pieChartDF = pd.DataFrame(, index = responseFrequencyKeys)
    '''

@application.route("/oneVarLongText", methods=['POST'])
def oneVarLongText():
    data = json.loads(request.data)
    srcList = []
    sentiment_analysis = {
        "very_positive": 0,
        "somewhat_positive": 0,
        "neutral": 0,
        "somewhat_negative": 0,
        "very_negative": 0
    }
    print(data)
    for response in data["first"]:
        polarity = TextBlob(response).sentiment.polarity
        if(polarity < -0.6):
            sentiment_analysis["very_negative"] += 1
        elif(polarity < -0.2):
            sentiment_analysis["somewhat_negative"] += 1
        elif(polarity < 0.2):
            sentiment_analysis["neutral"] += 1
        elif(polarity < 0.6):
            sentiment_analysis["somewhat_positive"] += 1
        else:
            sentiment_analysis["very_positive"] += 1
    print(sentiment_analysis)
    return("oneVarLongText success")



if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8081)
