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
    print("doing analysis for one variable number")
    data = json.loads(request.data)
    questionResponses = data["questionResponses"]
    s = pd.Series(questionResponses)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8081)