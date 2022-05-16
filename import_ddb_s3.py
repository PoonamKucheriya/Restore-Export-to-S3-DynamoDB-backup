import boto3
import json
import gzip
     
dynamo = boto3.client('dynamodb', region_name='us-west-2') 
s3 = boto3.client('s3')
 
# S3 Path to Exported data
s3Bucket = 'dynamodb-backup'
exportDataPrefix = 'test-account/AWSDynamoDB/1111111-9006e39a/data/'
DynamoDB_table = 'user-session'
 
# This script downloads all objects under the data/ folder and imports them back to DDB
export_objects = s3.list_objects(Bucket=s3Bucket, Prefix=exportDataPrefix)
 
for export_object in export_objects['Contents']:
	
	# Read objects
	s3_data_obj = s3.get_object(Bucket=s3Bucket, Key=export_object['Key'])
 
	# Import data into DDB using BatchWrite
	data = []
	with gzip.open(s3_data_obj['Body'], mode='rt') as items:
		for line in items:
			item = json.loads(line) 
			data.append({'PutRequest': item})
 
	# Batch write in batches of 20
	for i in range(0, len(data), 20):
		sub_arr = data[i:i + 20]
		print(sub_arr)
		dynamo.batch_write_item(RequestItems={DynamoDB_table: sub_arr})