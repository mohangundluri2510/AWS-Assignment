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


## Rohith`s approach--
