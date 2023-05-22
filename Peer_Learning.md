# AWS Peer Learning
<hr>

## Aswat Bisht`s code--
#### _Question-1_
* Configured the AWS ClI using **aws configure**
* Created policy which has S3 Full access <br>
* Created Role using cli <br>

```
aws iam create-role --role-name s3-role --assume-role-policy-document file://policy.json
```

* Attached the policy that created above to the role **s3-role** <br>
* Making a profile that uses the role <br>
* Created EC2 instance using the AWS CLI <br>

```
aws ec2 run-instances --image-id ami-0889a44b331db0194 --instance-type t2.micro --key-name demoKey --subnet-id subnet-0953ec6e2de22279d --security-group-ids sg-046ffd1222db8a6f3 --region us-east-1 --profile s3-role-profile
```

* Created the s3 bucket using cli <br>
```
aws s3api create-bucket --bucket gswbuck --region us-east-1 --profile s3-role-profile
```
<br>

#### _Question-2_

* Created a role with has access to put objects in the S3 bucket <br>
* Created Lambda Function using the AWS UI and attached the role **s3-put-object** <br>
* Created cloudwatch rule and attached it to the lambda function.
* The function generates the logs in the cloudwatch and it stops after 3 executions.

#### _Question-3_

* Created lambda function **putlns3Modified**  with accepts the parameters<br>
* Attached the **s3-put-object** role to the above lambda function. <br>
* Created api using AWS API Gateway, created api resources and created post method. Added mapping template in the application/json, tested the api. From postman send the given data to the api through post method
* The lambda function created the json files in the s3 buckets. <br>


## Rohith`s approach-- <br>

### Question-1: <br>
* Created Role using cli <br>
```
aws iam create-role --role-name rohith  --assume-role-policy-document file://trustpolicy.json
```
* Created policy which has full s3 access. <br>
* Attached the policy to the role. <br>
```
aws iam attach-role-policy --role-name rohith --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```
* Created instance profile <br>
```
aws iam create-instance-profile --instance-profile-name rohith_instance
```
* Attached the role to the instance profile <br>
```
aws iam add-role-to-instance-profile --instance-profile-name rohith_instance  --role-name rohith 
```

* Running the ec2 instance <br>
```
aws ec2 run-instances --image-id ami-0889a44b331db0194 --instance-type t3.micro --key-name rohith --iam-instance-profile Name="rohith_instance"
```
### Question-2:
Created a role and attached the policies and created a lambda function to put the files in the s3 bucket.
Generated the logs. <br>

```
import boto3
import datetime, time
import json

s3 = boto3.resource('s3')

bucket_name = 'rohiths3bucket1311'
key_name = 'transaction{}.json'

cw_logs = boto3.client('logs')
log_group = 'lambda_logs'
log_stream = 'lambda_stream'
count=0
def set_concurrency_limit(function_name):
    lambda_client = boto3.client('lambda')
    response = lambda_client.put_function_concurrency(
        FunctionName=function_name,
        ReservedConcurrentExecutions=0
    )
    print(response)
def lambda_handler(event, context):
    global count
    count+=1
    try:
        transaction_id = 12345
        payment_mode = "card/netbanking/upi"
        Amount = 200.0
        customer_id = 101
        Timestamp = str(datetime.datetime.now())
        transaction_data = {
            "transaction_id": transaction_id,
            "payment_mode": payment_mode,
            "Amount": Amount,
            "customer_id": customer_id,
            "Timestamp": Timestamp
        }
        
        # Save JSON file in S3 bucket
        json_data = json.dumps(transaction_data)
        file_name = key_name.format(Timestamp.replace(" ", "_"))
        s3.Bucket(bucket_name).Object(file_name).put(Body=json_data)
        
        # Log the S3 object creation event
        log_message = f"Object created in S3 bucket {bucket_name}: {file_name}"
        cw_logs.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[{
                'timestamp': int(round(time.time() * 1000)),
                'message': log_message
            }]
        )
        
        # Stop execution after 3 runs
        print(context)
        if count==1:
            print('First execution')
        elif count==2:
            print('Second execution')
        elif count==3:
            print('Third execution')
            print('Stopping execution')
            set_concurrency_limit('rohith-lambda')
    except Exception as exp:
        print(exp)
```
 
 ## Question-3: <br>
* Modified the lambda function which accepts the parameters.
```
import boto3
import datetime
import json

s3 = boto3.resource('s3')
bucket_name = 'rohiths3bucket1311'
key_name = 'file{}.json'

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

    except Exception as exp:
        print(e)
        return {
            "status": exp
        }
```

* Created api using amazon website , created resources and a post method.<br>
* Send the data using curl command through cli.
