from operator import contains
from flask import Flask, render_template, jsonify, request
import boto3
from boto3.dynamodb.conditions import Attr
import json


app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def hello_world():
    if request.method == "GET":
        json=getFreeParkings("Caserta", "10001")
        return render_template("index.html", result=json, length=len(json))
    else:
        city=request.form['cities']
        zone=request.form['zones']
        print (city,zone,"aaaa")
        json=getFreeParkings(str(city), str(zone))
        return render_template("index.html", result=json, length=len(json))

@app.route("/nearestParkings")
def nearestParkings():
    #json=getFreeParkings()
    return render_template("index.html", result=json, length=len(json))

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Parcheggio')

def getFreeParkings(city, zone): 
    response_text=dict()
    lista=list()
    stringa=""
    index=0
    db_response = table.scan(
        FilterExpression=(Attr('parking_area_city').eq(city)) & (Attr('parking_area_zone').eq(zone)) & (Attr('parking_area_free').eq(1))
    )
    for item in db_response['Items']:
        index=index+1
        item_lat = float(item['parking_area_latitude'])
        item_lon = float(item['parking_area_longitude'])
        response_text=({"latitude"+str(index)+"=": item_lat, "longitude"+str(index)+"=": item_lon})
        lista.append(response_text)
        print(response_text)
        #print (stringa)
    #val=json.loads(j)
    i=0
    coords_list=list()
    for item in lista:
        it=iter(item.values())
        coords_list.append(next(it))
        coords_list.append(next(it))
    #for key,value in response_text.items():
        #print(str(key)+" "+str(value), end='', flush=True)
    #print(j['latitude'])
    print(coords_list[0], "yoo")
    
    return coords_list

def call_function():
    client = boto3.client('lambda', endpoint_url="http://localhost:4566")
    
    

    response = client.invoke(
        FunctionName='Nearest_Parking_Area_Function',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=b'bytes'
    )