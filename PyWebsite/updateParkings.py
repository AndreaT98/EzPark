'''import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Parcheggio')




def getFreeParkings(): 
    response_text={}
    db_response = table.scan(
        FilterExpression=(Attr('parking_area_city').eq('Caserta')) & (Attr('parking_area_free').eq(1))
    )
    for item in db_response['Items']:
        item_lat = float(item['parking_area_latitude'])
        item_lon = float(item['parking_area_longitude'])
        response_text.update({"latitude": item_lat, "longitude": item_lon})
        json= (jsonify(response_text))
    #print (json)

getFreeParkings()

'''