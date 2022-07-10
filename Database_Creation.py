import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.create_table(
    TableName='Parkings',
    KeySchema=[
        {
            'AttributeName': 'parking_area_id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'parking_area_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print('Table', table, 'created!')

table = dynamodb.create_table(
    TableName='Zone',
    KeySchema=[
        {
            'AttributeName': 'zone_id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'zone_city',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'zone_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'zone_city',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print('Table', table, 'created!')