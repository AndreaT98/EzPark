from operator import contains
from flask import Flask, render_template, jsonify, request
import boto3
from boto3.dynamodb.conditions import Attr
import json

found=1
app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def hello_world():
    if request.method == "GET":
        return render_template("index.html")
    else:
        city=request.form['cities']
        zone=request.form['zones']
        print (city,zone,"aaaa")
        json=getFreeParkings(str(city), str(zone), "static_mode")
        return render_template("index.html", result=json, length=len(json), found=found, zone=zone)

@app.route("/nearestParkings", methods=('GET', 'POST'))
def nearestParkings():
    user_coordinates=[41.076448, 14.357053]
    json=getFreeParkings("Caserta", "10001", "user_mode")
    return render_template("index.html", result=json, length=len(json), found=0, user_coords=user_coordinates)




dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Parcheggio')

def getFreeParkings(city, zone, mode):
    client = boto3.client('lambda', endpoint_url="http://localhost:4566")
    if mode == "static_mode":
        payload= '{"city": "'+city+'", "zone": "'+zone+'", "mode": "static_mode"}'
    elif mode == "user_mode":
        payload= '{"city": "'+city+'", "zone": "'+zone+'","mode": "user_mode"}'
    

    response = client.invoke(
        FunctionName='Nearest_Parking_Area_Function',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=payload
    )
    coords_list= decode_response(response)
    return coords_list

def call_function():
    client = boto3.client('lambda', endpoint_url="http://localhost:4566")
    


    response = client.invoke(
        FunctionName='Nearest_Parking_Area_Function',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=b'bytes'
    )

def decode_response(data):
    data = data['Payload'].read().decode()
    global found
    coords_list=[]
    js = json.loads(data)
    js_len=len(js)
    if -1 in js:
        print ("SET FOUND TO 0!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        found=0
        js.pop()
    else:
        found=1
    print(js)
    if js_len!=0:
        for i in range(len(js)):
            print (js[i])
            for value in js[i].values():
                print (value)
                coords_list.append(value)  
    return coords_list
