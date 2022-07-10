import boto3
import random

sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

cities = [('Salerno', 5), ('Caserta', 3), ('Napoli', 6), ('Benevento', 2), ('Avellino', 3)]
parking_areas=[('1', '41.0737547', '14.3563383', random.randint(0, 1), 'Caserta', 'Via Rossi'),
 ('2', '41.0737997', '14.3563568', random.randint(0, 1), 'Caserta', 'Via Rossi'),
 ('3', '41.0750437', '14.3570320', random.randint(0, 1), 'Caserta', 'Via Verdi'),
 ('4', '41.0750480', '14.3569251', random.randint(0, 1), 'Caserta', 'Via Verdi'),
 ('5', '41.0750934', '14.3569521', random.randint(0, 1), 'Napoli', 'Via Verdi'),
 ('6', '41.0750480', '14.3569621', random.randint(0, 1), 'Napoli', 'Via Verdi'),
 ('7', '41.0750480', '14.3569721', random.randint(0, 1), 'Caserta', 'Via Verdi'),
 ('8', '41.0750480', '14.3569821', random.randint(0, 1), 'Salerno', 'Via Verdi'),]
user_position=[('41.0747385', '14.3571234')] 
i=0

for id, latitude, longitude, free, city, zone in parking_areas:
	i=i+1
	queue = sqs.get_queue_by_name(QueueName=city+"_sensors")
	msg_body = '{"parking_area_id": "%s","latitude": "%s","longitude": "%s","free": "%s","city": "%s","zone": "%s"}' \
			% (id, latitude, longitude, free, city, zone)
	queue.send_message(MessageBody=msg_body)
