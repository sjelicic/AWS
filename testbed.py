import boto3

region = 'eu-central-1'
instances = ['i-0be8b10d10f8ab393']

def lambda_handler(event, context):
	ec2 = boto3.client('ec2', region_name=region)
	ec2.stop_instances(InstanceIds=instances)
	print 'stopped the instance: ' + str(instances)