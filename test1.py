import boto3
from pprint import pprint

#koristimo resource umesto client
ec2 = boto3.resource('ec2')

print(ec2.instances)

def lambda_handler(event, context):
	#filteri bre
	filters = [
		{
			'Name': 'instance-state-name',
			#'Values': ['running']
			'Values': ['stopped']
		}
	]

	#filtrira instance na osnovu filtera gore
	instances = ec2.instances.filter(Filters=filters)

	#stvara prazan niz
	RunningInstances= []

	for instance in instances:
		#for each instance, append to array and print instance id
		RunningInstances.append(instance.id)
		print(instance.id)

