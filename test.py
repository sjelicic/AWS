import boto3
from pprint import pprint

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()

pprint(response)
print('\n')

test = 'adsfjlakdjs'

pprint('test')

for reservation in response['Reservations']:
	for instance in reservation['Instances']:
		#prints the entire dictionary object
		pprint(instance)
		#prints value of the dictionary key 'InstanceID'
		print('\n')
		pprint(instance['InstanceId'])
		pprint(instance['LaunchTime'])

