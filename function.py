import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def logging_handler(event, context):
	logger.info('received event{}'.format(event))
	#Convert a value to a “formatted” representation, as controlled by format_spec. 
	#The interpretation of format_spec will depend on the type of the value argument, 
	#however there is a standard formatting syntax that is used by most built-in types: 
	#The default format_spec is an empty string which usually gives the same effect as calling str(value).
	
	#This “new style” (str.format) string formatting gets rid of the %-operator special syntax and makes the syntax for string formatting more regular. 
	#Formatting is now handled by calling .format() on a string object.
	#You can use format() to do simple positional formatting, just like you could with “old style” formatting:
	#>>> 'Hello, {}'.format(name)
	#'Hello, Bob'

	logger.error('Something went wrong')




print('Starting new invocation')
logger.info('Starting new invocation')

def lambda_handler(event, context):
	bucket = event['Records'][0]['s3']['bucket']['name']
	region = event['Records'][0] ['awsRegion']
	object = event['Records'][0]['s3']['object']['key']
	user = event['Records'][0]['userIdentity']['principalId']

	logger.info('Bucket: ' + bucket)
	logger.info('Region: ' + region)
	logger.info('User is: ' + user)

	return(object)


