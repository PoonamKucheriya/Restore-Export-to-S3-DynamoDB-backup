import boto3
import json
import gzip


# Replace with ARN of your limited DynamoDB role:
role_to_assume_arn = "arn:aws:iam::1111111111:role/Restore-eRole"
role_session_name = "test_session"

# S3 Path to Exported data
s3Bucket = 'dynamodb-backup'
exportDataPrefix = 'test-account/AWSDynamoDB/1111111-9006e39a/data/'
region_name='us-west-2'
DynamoDB_table = 'user-session'

sts = boto3.client("sts")

print("Default Provider Identity: : " + sts.get_caller_identity()["Arn"])

response = sts.assume_role(
    RoleArn=role_to_assume_arn, RoleSessionName=role_session_name, DurationSeconds=43200,
)

creds = response["Credentials"]

sts_assumed_role = boto3.client(
    "sts",
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"],
)

print("AssumedRole Identity: " + sts_assumed_role.get_caller_identity()["Arn"])

# Create boto3 client with assumed role

dynamo = boto3.client(
    'dynamodb',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken'],
    region_name=region_name
)

s3 = boto3.client(
    's3',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken'],
)

 
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