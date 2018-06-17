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
    srcData = {}
    data = json.loads(request.data)
    print(data)
    fig = plt.figure()
    plot = sns.countplot(data["first"])
    plot.set(xlabel=data["firstQuestionField"], ylabel="frequency")
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)

    print (base64.encodebytes(imgdata.getvalue()).decode())
    print ("Content-type: image/png\n")
    uri = 'data:image/png;base64,' + base64.encodebytes(imgdata.getvalue()).decode()
    print ('<img src = "%s"/>' % uri)
    return "success"


    #piechart below
    """ {‘first’: [‘Brazil’, ‘Brazil’, ‘Brazil’, ‘Portugal’, ‘Germany’, ‘Germany’, ‘Argentina’, ‘Argentina’, ‘Brazil’, ‘Germany’], ‘firstQuestionField’: ‘Who do you think will win the World Cup?’}"""
    responseFrequencyComplete = collections.Counter(data['first'])
    responseFrequencyKeys = responseFrequencyComplete.keys()
    responseFrequencyValues = responseFrequencyComplete.values()

    pieChartDF = df = pd.DataFrame({'mass': responseFrequencyValues}, index = responseFrequencyKeys)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8081)
