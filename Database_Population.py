import boto3
import datetime
import random

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Parkings')
41.074013, 14.356446
zones = [
    ('10001', 'Via Rossi', 'Caserta', '41.0739081', '14.3564235'), 
    ('10002', 'Via Verdi', 'Caserta', '41.074013', '14.356446'), 
    ('10003', 'Via Verdi', 'Napoli', '41.0750649', '14.3566230'),
    ('10004', 'Via Verdi', 'Napoli', '41.0750649', '14.3566230'),
    ('10005', 'Via Verdi', 'Salerno', '41.0750649', '14.3566230'),
    ('10006', 'Via Verdi', 'Salerno', '41.0750649', '14.3566230')]
parking_areas=[('1', '41.0737547', '14.3563383', 0, 'Caserta', '10001'),
 ('2', '41.0737997', '14.3563568', 0, 'Caserta', '10001'),
 ('3', '41.0750437', '14.3570320', 1, 'Caserta', '10002'),
 ('4', '41.0750480', '14.3569251', 1, 'Caserta', '10002'),
 ('5', '41.0750934', '14.3569521', 0, 'Napoli', '10002'),
 ('6', '41.0750480', '14.3569621', 0, 'Napoli', '10002'),
 ('7', '41.0750480', '14.3569721', 0, 'Caserta', '10002'),
 ('8', '41.0750480', '14.3569821', 1, 'Salerno', '10002'),]

'''41,0737547 14,3563383
41,0737997 14,3563568

41,0750437 14,3570320
41,0750480 14,3569251

device_ids = []

for city, device_id in cities:
    city_devices = ""
    for i in range(device_id):
        city_devices = city_devices + ("%s_%s") % (city, str(i)) + " "
    device_ids.append(city_devices)'''

for i in range(len(parking_areas)):
    item = {
        'parking_area_id': parking_areas[i][0],
        'parking_area_latitude': parking_areas[i][1], 
        'parking_area_longitude': parking_areas[i][2],
        'parking_area_free': parking_areas[i][3],
        'parking_area_city': parking_areas[i][4],
        'parking_area_zone': parking_areas[i][5]
    }
    table.put_item(Item=item)

    print("Stored item", item)

table = dynamodb.Table('Zone')

for i in range(len(zones)):
    item = {
        'zone_id': zones[i][0],
        'zone_name': zones[i][1], 
        'zone_city': zones[i][2],
        'zone_latitude': zones[i][3],
        'zone_longitude': zones[i][4],
    }
    table.put_item(Item=item)

    print("Stored item", item)