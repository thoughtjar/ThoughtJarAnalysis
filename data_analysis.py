from flask import Flask, request, send_file, jsonify
import matplotlib
matplotlib.use('Agg')
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

#test display
plt.plot([1,2,3])
plt.show()


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

    # boxplot
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
    #histogram
    #sample request {'first': ['3', '1', '8', '4', '3'], 'firstQuestionField': 'How many games do you think Portugal win?'}


    # doing in notebook then will paste here later



    srcData = {"srcList": srcList}
    print(srcData)
    print(type(srcData))
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

    #matplotlib piechart
    #hardcodedData = {'first': ['Brazil', 'Brazil', 'Brazil', 'Portugal', 'Germany', 'Germany', 'Argentina', 'Argentina', 'Brazil', 'Germany'], 'firstQuestionField': 'Who do you think will win the World Cup?'}
    responseFrequencyComplete = collections.Counter(data['first'])
    responseFrequencyKeys = responseFrequencyComplete.keys()
    responseFrequencyValues = responseFrequencyComplete.values()

    labels = responseFrequencyKeys
    sizes = responseFrequencyComplete.values()
    # no explode
    explode = (0, 0, 0, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    plt.tight_layout()
   # plt.show() shows the plot

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    #figdata_png is the x64 string
    figdata_png = base64.b64encode(figfile.getvalue()).decode('ascii')
    srcList.append(figdata_png)

    srcData = {"srcList": srcList}
    return jsonify(srcData)



@application.route("/oneVarLongText", methods=['POST'])
def oneVarLongText():
    data = json.loads(request.data)
    srcList = []
    sentiment_analysis = []
    sentiment_subjectivity = []
    print(data)
    for response in data["first"]:
        polarity = TextBlob(response).sentiment.polarity
        subjectivity = TextBlob(response).sentiment.subjectivity
        print(polarity)
        print(subjectivity)
        if(polarity < -0.4):
            sentiment_analysis.append("very negative")
        elif(polarity < -0.1):
            sentiment_analysis.append("somewhat negative")
        elif(polarity < 0.1):
            sentiment_analysis.append("neutral")
        elif(polarity < 0.4):
            sentiment_analysis.append("somewhat positive")
        else:
            sentiment_analysis.append("very positive")
        if(subjectivity < 0.1):
            sentiment_subjectivity.append("objective")
        elif(subjectivity < 0.4):
            sentiment_subjectivity.append("somewhat subjective")
        else:
            sentiment_subjectivity.append("very subjective")

    #sentiment analysis
    sentiment_data = pd.Series(sentiment_analysis)
    fig = plt.figure()
    plot = sns.countplot(sentiment_data, order=["very negative", "somewhat negative", "neutral", "somewhat positive", "very positive"])
    title = "Sentiment Analysis: " + data["firstQuestionField"]
    plot.set(xlabel=title, ylabel="frequency")
    plot.set_xticklabels(plot.get_xticklabels(), fontsize=8)
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    src = base64.encodebytes(imgdata.getvalue()).decode()
    print(src)
    srcList.append(src)

    #subjectivity analysis
    subjectivity = pd.Series(sentiment_subjectivity)
    fig = plt.figure()
    plot = sns.countplot(subjectivity, order=["objective", "somewhat subjective", "very subjective"])
    title = "Subjectivity Analysis: " + data["firstQuestionField"]
    plot.set(xlabel=title, ylabel="frequency")
    plot.set_xticklabels(plot.get_xticklabels(), fontsize=8)
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    src = base64.encodebytes(imgdata.getvalue()).decode()
    print(src)
    srcList.append(src)
    srcData = {"srcList": srcList}
    return jsonify(srcData)

@application.route("/twoVarNumNum", methods=['POST'])
def twoVarNumNum():
    data = json.loads(request.data)
    print(data)
    srcList = []
    firstQuestionResponses = []
    secondQuestionResponses = []
    for stringNum in data["first"]:
        firstQuestionResponses.append(int(stringNum))
    for stringNum in data["second"]:
        secondQuestionResponses.append(int(stringNum))
    # scatterplot with regression
    first = pd.Series(firstQuestionResponses)
    second = pd.Series(secondQuestionResponses)
    fig = plt.figure()
    plot = sns.regplot(x=first, y=second)
    plot.set(xlabel=data["firstQuestionField"], ylabel=data["secondQuestionField"])
    imgdata = BytesIO()
    fig.savefig(imgdata, format="png")
    imgdata.seek(0)
    src = base64.encodebytes(imgdata.getvalue()).decode()
    print(src)
    srcList.append(src)

    srcData = {"srcList": srcList}
    return jsonify(srcData)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8081)
