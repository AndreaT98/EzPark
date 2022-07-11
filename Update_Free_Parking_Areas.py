import boto3
import datetime

def lambda_handler(event, context):
	dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
	ses = boto3.client('ses', endpoint_url='http://localhost:4566')

	table = dynamodb.Table('Parkings')
	message = []

	for update in event:
		if (update[3] != '-1'):
			table.update_item(
				TableName='Parkings',
				Key={'parking_area_id': update[0]
				},
				ConditionExpression='attribute_exists(parking_area_id)',
				UpdateExpression='SET parking_area_free = :val',
				ExpressionAttributeValues = {':val': update[3]}
			)
			message.append("Item "+update[0]+" has been put in database")
			
		else:
			message.append("Item "+update[0]+" has generated an error")
			ses.send_email(
			Source='amazon-aws@amazon.com',
			Destination={
				'ToAddresses': [
					'user@example.com',
				]
			},
			Message={
				'Subject': {
					'Data': 'Sensor of ID='+update[0]+' has generated an error!',
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
			
	return message