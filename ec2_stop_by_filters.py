import boto3
import logging

logger = logging.getLogger()
#Loggers are never instantiated directly, 
#but always through the module-level function logging.getLogger(name). 

logger.setLevel(logging.INFO)
#setLevel(level)
#Sets the threshold for this logger to level. 
#Logging messages which are less severe than level will be ignored; 
#Changed in version 3.2: The level parameter now accepts a string representation 
#of the level such as ‘INFO’ as an alternative to the integer constants such as INFO. 

#Logging Levels
# Level		Numeric value
# CRITICAL		50
# ERROR			40
# WARNING		30
# INFO			20
# DEBUG			10
# NOTSET		0

#define the connection
ec2 = boto3.resource('ec2','eu-central-1')

#definisao filter (jebali me filteri)
def lambda_handler(event, context):
	filters= [{'Name':'tag:Sloba', 'Values':['car']}]

	#filtrira instance (jebalo me filtriranje)
	instances = ec2.instances.filter(Filters=filters)
	#filter() function returns an iterator were the items are filtered through a function 
	#to test if the item is accepted or not.
	#The EC2 instances collection takes a parameter called Filters which is a list of names and values,

	# instances = ec2.instances.filter(
	#     Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	# for instance in instances:
	#     print(instance.id, instance.instance_type)

	#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

	for instance in instances:
		print(instance.id, instance.instance_type)

	RunningInstances = [instance.id for instance in instances]
	print(RunningInstances)

	print ('\n')

	ShutDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
	print(ShutDown)



