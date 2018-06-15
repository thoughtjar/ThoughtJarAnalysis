from flask import Flask, request, send_file
import csv
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
    return src

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8081)
