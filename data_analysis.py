from flask import Flask, request, send_file
import csv
import json
'''
import boto3

s3 = boto3.client('s3')
filename = "data.csv"
bucket_name = "thoughtjardata"
'''
application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"

@application.route("/csv", methods=['POST'])
def getCSV():
    print("CSVVVVVV")
    data = json.loads(request.data)
    print(type(data))
    print(data["responseContent"])
    #rint(request.data)
    responseContent = data["responseContent"]
    print("hERE")
    print(list(responseContent[0].keys()))
    f = csv.writer(open("data.csv", "w"))
    f.writerow(list(responseContent[0].keys()))
    for response in responseContent:
        row = []
        for key in responseContent[0].keys():
            row.append(response[key])
        print(row)
        f.writerow(row)
    #s3.upload_file(filename, bucket_name, filename)

    with open('data.csv') as f:
        s = f.read() + '\n'
    return s

    #return "hi"

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8081)
