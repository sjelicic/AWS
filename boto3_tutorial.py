import boto3
from pprint import pprint


ec2 = boto3.client('ec2')
response = ec2.describe_instances()

pprint(response)