# Restore-Export-to-S3-DynamoDB-backup

[How to utilise “Export to S3” DynamoDB backup to restore DynamoDB table](https://poonamkucheriya.wordpress.com/2020/12/08/how-to-utilise-export-to-s3-dynamodb-backup-to-restore-dynamodb-table/)

We all loved the new Export to S3 backup feature shared by DynamoDB but we can not restore the table again. I came up with a workaround to achieve that using a Python script. This script can also be used to restore backup from cross account s3 bucket and also for cross region DynamoDB tables.

Below article will utilise **“Export to S3”** backup to restore the table in same account, cross-account and in cross region as well.  Basically Script points to the exported S3 bucket location, fetches the .json.gz, converts backups in BatchWrite API acceptable format and inserts them in the table using BatchWrite operation.

1. It utilises one button click “Export to s3” backup, which is of no use at the moment if you want to import it back 

2. No need to Spin up Data Pipeline for export and import

3. I won’t recommend using this for a huge dataset as we are using assume roles [temporary credentials] to get a cross account bucket and DynamoDB table. They do expire so the process will be interrupted. 

Test this in your test environment and once you think you are happy with the results, they can use it for other tables. 

Now time to share steps you need to follow to run this script:

1. Script is written in Python, so machine from which you are running must have python3 installed along with AWS SDK for Python (Boto3) [1][2][3]

2. The AWS cli should have credentials of the role which have s3 bucket access and DynamoDB table access[In case of cross account role must have cross account access {4}].

3. Once all the setup is done, verify if the script has the right region, right S3 path to backup and right DynamoDB table name, right role arn which have all necessary accesses. You should run this script from the account where the new DynamoDB table resides, also a table must be created prior to running this script so that it will import data. 

Finally time to run the script Finally time to run the script

>> Python3 import_ddb_s3.py

You can verify if data is inserted correctly via AWS Management console.

4. Once import is done, you may unset credentials using below command, if not they will anyways expire after 12 hours.

unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN

I would greatly appreciate your feedback on this script and if it helped you !! 

Reference:

[1] https://www.python.org/downloads/

[2] https://aws.amazon.com/sdk-for-python/

[3] https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

[4] https://aws.amazon.com/premiumsupport/knowledge-center/cross-account-access-s3/
