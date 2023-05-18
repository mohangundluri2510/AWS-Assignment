# AWS-Assignment
<hr>


**Creating role with S3 Full access** <br>

```
aws iam create-role --role-name mohan-gundluri-1  --assume-role-policy-document file://trust_policies_q1.json
```
<img width="1119" alt="Screenshot 2023-05-17 at 1 59 09 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/759fd13b-3114-411f-858f-b3324be03fc7">
<br>

**Attaching the policy to the role** <br>
```
aws iam attach-role-policy --role-name mohan-gundluri-1 --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```
<img width="1119" alt="Screenshot 2023-05-17 at 2 16 39 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/d398b61c-80d3-4407-9a98-2f87dd857a9f">
<br>

**Creating EC2 instance profile with the mohan-gundluri-1 role** <br>
```
aws iam create-instance-profile --instance-profile-name mohan_instance_prof_1
```
<img width="1119" alt="Screenshot 2023-05-17 at 4 00 11 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/570d1d73-9a2c-4e2b-a413-3057ad19c491">
<br>

**Adding role mohan-gundluri-1 to the instance profile mohan_instance_prof_1** <br>
```
aws iam add-role-to-instance-profile --instance-profile-name mohan_instance_prof_1 --role-name mohan-gundluri-1
```

**Run the EC2 instance** <br>
```
aws ec2 run-instances --image-id ami-0889a44b331db0194 --instance-type t2.micro --key-name mohan-aws-keypair --security-group-ids sg-066205334fd658af6 --iam-instance-profile Name=mohan_instance_prof_1 --region us-east-1
```
<br>
<img width="1188" alt="Screenshot 2023-05-17 at 4 24 20 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/a815749b-e89b-4176-a669-22506ad3aa10"><br>

**Creating S3 bucket using the role mohan-gundluri-1** <br>

```
aws s3api create-bucket --bucket aws-assignment-bucket-01 --region us-east-1  --acl private
```
<img width="1188" alt="Screenshot 2023-05-17 at 4 34 31 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/c875a51d-8076-4211-84f2-cc546e0ded25">
<br>


### Question-2

**Put the files in the S3 bucket** <br>
**Creating the policy which has S3 put access** <br>
```
# Creating policy
def createPolicy(policy_name, policy_document):
    try:
        response = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        return response
    except ClientError as e:
        print("There is an Error while creating IAM policy:", e)

policy_name = 'LambdaS3PutPolicy'
policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject"],
                "Resource": ["arn:aws:s3:::aws-assignment-bucket-01/*"]
            }
        ]
    }
policy_arn = createPolicy(policy_name, policy_document)['Policy']['Arn']
```
**Creating the new role for the AWS Lambda** <br>
```
# Creating role
def createRole(role_name, role_policy_document):
    try:
        role_response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(role_policy_document)
        )
    except ClientError as e:
        print(f"There is an Error while creating role, {e}")
 
 role_name = "AWSLambdaS3PutAccessRole"
role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
}


createRole(role_name, role_policy_document)
```
<br>
**Attaching the policy to the role** <br>

```
# Attach the necessary policy for S3 put access
def attachRolePolicy(role_name, policy_arn):
    try:
        attach_response = iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        return attach_response
    except ClientError as e:
        print(f"There is an Error while attaching policy to role, {e}")
        
        
attachRolePolicy(role_name, policy_arn)
```

**Create new policy which writes the logs** <br>

```
cloudwatch_policy_name = 'AWSCloudWatchLogsPolicyMohan'
cloudwatch_policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:GetLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

<br>
**Attach the new policy to the above role** <br>

```
attachRolePolicy(role_name, cloudwatch_logs_policy_arn)
```

<img width="1159" alt="Screenshot 2023-05-17 at 6 31 22 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/39ee8c0b-c3bb-4899-a834-00fdc08e8937">

<br>

**Created Lambda Function with the above role** <br>

Schedule the task to run every minute and stop execution after 3 runs <br>
* Create a rule in cloud watch events with cron expression cron( "* * * * ? *") to trigger above created lambda function.<br>

```
import boto3
import datetime, time
import json

s3 = boto3.resource('s3')

bucket_name = 'aws-assignment-bucket-01'
key_name = 'payment{}.json'

logs_client = boto3.client('logs')


count = 0

def lambda_handler(event, context):
    global count
    count += 1
    try:
        # Generate JSON in the given format
        transaction_id = 12345
        payment_mode = "card/netbanking/upi"
        amount = 200.0
        customer_id = 101
        timestamp = str(datetime.datetime.now())

        transaction_data = {
            "transaction_id": transaction_id,
            "payment_mode": payment_mode,
            "amount": amount,
            "customer_id": customer_id,
            "timestamp": timestamp
        }

        # Save JSON file in S3 bucket
        json_data = json.dumps(transaction_data)
        file_name = key_name.format(timestamp.replace(" ", "_"))
        s3.Bucket(bucket_name).Object(file_name).put(Body=json_data)

        # Log the S3 object creation event
        log_group = 'Mohan_Logs_group'
        log_stream = 'Mohan_log_stream_data'
        log_message = f"Object created in the S3 bucket {bucket_name}"
        logs_client.create_log_group(logGroupName=log_group)
        logs_client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
        logs_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[{
                'timestamp': int(round(time.time() * 1000)),
                'message': log_message
            }]
        )

        # Stop execution after 3 runs
        if count == 1:
            print('First execution')
        elif count == 2:
            print('Second execution')
        elif count == 3:
            print('Third execution')
        else:
            print('Stopping execution')
            return

    except Exception as e:
        print(e)

```
<br>
**Generated the logs** <br>
<img width="1159" alt="Screenshot 2023-05-18 at 3 35 36 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/2d7addd6-f7b2-44f7-bc3e-f1e98242bacb">
<br>

### Question-3 <br>


**Modify lambda function to accepts the parameters.** <br>
```
import boto3
import datetime
import json

s3 = boto3.resource('s3')
bucket_name = 'aws-assignment-bucket-01'
key_name = 'payment1{}.json'


def lambda_handler(event, context):
    try:
        # Parse input data
        body = event['body']
        timestamp = str(datetime.datetime.now())
        body["timestamp"] = timestamp

        # Save JSON file in S3 bucket
        json_data = json.dumps(body)
        file_name = key_name.format(timestamp.replace(" ", "_"))
        s3.Object(bucket_name, file_name).put(Body=json_data)

        # Log the S3 object creation event
        print(f"Object created in S3 bucket {bucket_name}: {file_name}")

        return {
            "file_name": file_name,
            "status": "success"
        }

    except Exception as e:
        print(e)
        return {
            "status": "error"
        }
```

<br>

* Create a POST API from API Gateway, pass parameters as request body to Lambda job. Return the filename and status code as a response.<br>
* Create api in the amazon api gateway ,create the resource and create post method in the resource. <br>
 
 <img width="1159" alt="Screenshot 2023-05-18 at 4 00 07 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/32d85338-dd65-4157-b2c5-1a643bc0ed10">
 
<br>

**Sent data from the postman** <br>
<img width="1440" alt="Screenshot 2023-05-18 at 4 06 41 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/4eaa2c2f-884e-451a-b69c-749cdb12b065">
<br>

**Generated the logs in cloud watch**  <br>
<img width="1440" alt="Screenshot 2023-05-18 at 4 07 24 PM" src="https://github.com/mohangundluri2510/AWS-Assignment/assets/123619711/b2adae07-269f-464b-b1c2-b75dd2a2d047">


