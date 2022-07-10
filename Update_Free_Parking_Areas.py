import boto3
import datetime
import json


def lambda_handler(event, context):
	dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
	sqs_client = boto3.client('sqs', endpoint_url='http://localhost:4566')
	ses = boto3.client('ses', endpoint_url='http://localhost:4566')

	table = dynamodb.Table('Parcheggio')

	cities = ['Caserta', 'Napoli', 'Salerno']


	for city in cities:
		messages=[]
		#response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
		response = sqs_client.receive_message(
			QueueUrl='http://localhost:4566/000000000000/'+city+'_sensors',
			AttributeNames=[
				'All'
				],
			MaxNumberOfMessages=10,
			VisibilityTimeout=10,
			WaitTimeSeconds=10,
			)
		if(response):
			messages=response.get("Messages", [])
			for message in messages:
				message_body = message["Body"]
				content=json.loads(message_body)
				list_of_values=list(content.values())
				receipt_handle=message['ReceiptHandle']
				if (list_of_values[3] != '-1'):
					table.update_item(
						TableName='Parcheggio',
						Key={'parking_area_id': list_of_values[0]
						},
						ConditionExpression='attribute_exists(parking_area_id)',
						UpdateExpression='SET parking_area_free = :val',
						ExpressionAttributeValues = {':val': list_of_values[3]}
					)
					response = sqs_client.delete_message(
					QueueUrl="http://localhost:4566/000000000000/"+city+"_sensors",
					ReceiptHandle=receipt_handle,
					)
				else:
					ses.send_email(
                    Source='amazon-aws@amazon.com',
                    Destination={
                        'ToAddresses': [
                            'a.tranquillo1@studenti.unisa.it',
                        ]
                    },
                    Message={
                        'Subject': {
                            'Data': 'Sensor of ID='+list_of_values[0]+' has generated an error!',
                            'Charset': 'utf-8'
                        },
                        'Body': {
                            'Text': {
                                'Data': 'Hello from Amazon AWS. This message has been sent to you because one of your sensor in date '+str(datetime.datetime.now())+' generated error. Please take care of it!',
                                'Charset': 'utf-8'
                            }
                        }
                    },
                )