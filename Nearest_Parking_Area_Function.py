from math import radians, cos, sin, asin, sqrt
import boto3
from boto3.dynamodb.conditions import Attr


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('Parkings')
    table_zone = dynamodb.Table('Zone')
    lista=list()
    user_coordinates=[41.076448, 14.357053]

    if event['city'] and event['mode']=="static_mode":
        db_response = table.scan(
            FilterExpression=(Attr('parking_area_zone').eq(event['zone'])) & (Attr('parking_area_city').eq(event['city']))
        )
        trovato = 0
        free_parkings = []
        for item_db in db_response['Items']:
            free = int(item_db['parking_area_free'])
            if(free == 1):
                trovato = 1
                free_parkings.append(
                    (item_db['parking_area_latitude'], item_db['parking_area_longitude']))
        if(trovato == 0):
            db_response = table_zone.scan(
                FilterExpression=Attr('zone_city').eq(event['city'])
            )
            for item_ in db_response['Items']:
                item_lat = float(item_['zone_latitude'])
                item_lon = float(item_['zone_longitude'])
                lista = find_free_parking_areas_nearby(
                    item_lat, item_lon, event['city'])
                lista.append(-1)
        else:
            for i in range(len(free_parkings)):
                response_text=({"latitude=": free_parkings[i][0], "longitude=": free_parkings[i][1]})
                lista.append(response_text)
        return lista
    elif "user_mode"==event['mode']:
        lista=list()
        lista=find_free_parking_areas_nearby(user_coordinates[0], user_coordinates[1], "Caserta")
        return lista


def find_free_parking_areas_nearby(lat, lon, city):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

    table = dynamodb.Table('Parkings')

    spots = []

    db_response = table.scan(
        FilterExpression=Attr('parking_area_city').eq(city) & Attr('parking_area_free').eq(1)
    )

    for item in db_response['Items']:
        item_lat = float(item['parking_area_latitude'])
        item_lon = float(item['parking_area_longitude'])
        distance = calculate_distance(lat, lon, item_lat, item_lon)
        if(distance < 0.3 ):
            response_text=({"latitude=": item_lat, "longitude=": item_lon})
            spots.append(response_text)
    return spots


def calculate_distance(lat1, lon1, lat2, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers
    r = 6371

    # calculate the result
    return(c * r)
