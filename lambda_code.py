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
