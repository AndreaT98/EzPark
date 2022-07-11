from flask import Flask, render_template, request
import boto3
import json

found=1
app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        city=request.form['cities']
        zone=request.form['zones']
        result=getFreeParkings(str(city), str(zone), "static_mode")
        return render_template("index.html", result=result, length=len(result), found=found, zone=zone)

@app.route("/nearestParkings", methods=('GET', 'POST'))
def nearestParkings():
    user_coordinates=[41.076448, 14.357053]
    result=getFreeParkings("Caserta", "10001", "user_mode")
    return render_template("index.html", result=result, length=len(result), found=0, user_coords=user_coordinates)




dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Parkings')

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

def decode_response(data):
    data = data['Payload'].read().decode()
    global found
    coords_list=[]
    js = json.loads(data)
    js_len=len(js)
    print (js)
    if -1 in js:
        found=0
        js.pop()
    else:
        found=1
    if js_len!=0:
        for i in range(len(js)):
            for value in js[i].values():
                coords_list.append(value)  
    return coords_list
