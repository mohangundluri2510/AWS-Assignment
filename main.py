import boto3
import json
from botocore.exceptions import ClientError

iam_client = boto3.client('iam')


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


# Creating role
def createRole(role_name, role_policy_document):
    try:
        role_response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(role_policy_document)
        )
    except ClientError as e:
        print(f"There is an Error while creating role, {e}")


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
attachRolePolicy(role_name, policy_arn)


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

# Creating policy AWSCloudWatchLogsPolicyMohan and getting its arn
cloudwatch_logs_policy_arn = createPolicy(policy_name=cloudwatch_policy_name,
                                          policy_document=cloudwatch_policy_document)['Policy']['Arn']

# Attaching AWSCloudWatchLogsPolicyMohan policy to the role AWSLambdaS3PutAccessRole
attachRolePolicy(role_name, cloudwatch_logs_policy_arn)
