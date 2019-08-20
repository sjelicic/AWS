from __future__ import print_function
import json
import boto3
import logging
import time
import datetime



logger = logging.getLogger()                    #<- logger object
#Note that Loggers are never instantiated directly, but always through the module-level function logging.getLogger(name). 
#Multiple calls to getLogger() with the same name will always return a reference to the same Logger object.

logger.setLevel(logging.INFO)
#Sets the threshold for this logger to level. 
# Logging messages which are less severe than level will be ignored; 
# logging messages which have severity level or higher will be emitted by whichever handler or handlers service this logger, 
# unless a handler’s level has been set to a higher severity level than level.

# Level       Numeric value
# CRITICAL        50
# ERROR           40
# WARNING         30
# INFO            20
# DEBUG           10
# NOTSET          0


# Rules > New-EC2Resource-Event                     <- event-ovi koji f-ja lambda_handler prima

#     "eventName": [
#       "CreateVolume",
#       "RunInstances",
#       "CreateImage",
#       "CreateSnapshot"


def lambda_handler(event, context):
    #logger.info('Event: ' + str(event))
    #print('Received event: ' + json.dumps(event, indent=2))
 
# event – AWS Lambda uses this parameter to pass in event data to the handler. This parameter is usually of the Python dict type. 
#It can also be list, str, int, float, or NoneType type.

# It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within
# one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs
# within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on
# output.


    #test (zelim da odstampam citav event, listam sve key:pair vrednosti u okviru dictionary-a)
    # for k, v in event.items():          
    #     print(k, v)
        
    #odstampane vrednosti koje f-ja koristi    
    # print('fuck you faggot')
    # print(event['region'])
    # print(event['detail'])
    # print(detail['eventName'])
    # print(detail['userIdentity']['arn'])
    # print(detail['userIdentity']['principalId'])
    # print(detail['userIdentity']['type'])
    #print(detail['userIdentity']['userName'])
    
    #koristi se nakon sto podignem ec2 resurs
    ids = []                            #<- inicijalizuje listu


    #The try block lets you test a block of code for errors.
    # When an error occurs, or exception as we call it, Python will normally stop and generate an error message.
    # These exceptions can be handled using the try statement:

    # The try block will generate an exception, because x is not defined:

    # try:
    #   print(x)
    # except:
    #   print("An exception occurred")
    #Since the try block raises an error, the except block will be executed.

    #A try statement may have more than one except clause, to specify handlers for different exceptions.
    try:
        region = event['region']                            #<- ovo su sve relevantni detalji iz event-a koji je prosledjen f-ji lambda_handler
        detail = event['detail']
        eventname = detail['eventName']
        arn = detail['userIdentity']['arn']
        principal = detail['userIdentity']['principalId']
        userType = detail['userIdentity']['type']

        if userType == 'IAMUser':
            user = detail['userIdentity']['userName']

        else:
            user = principal.split(':')[1]

        #info(msg, *args, **kwargs)
        #Logs a message with level INFO on this logger. 
        logger.info('principalId: ' + str(principal))       <- #detalji logger objekta
        logger.info('region: ' + str(region))                   #output se moze videti u CloudWatch logu
        logger.info('eventName: ' + str(eventname))
        logger.info('detail: ' + str(detail))

        #https://stackoverflow.com/questions/100732/why-is-if-not-someobj-better-than-if-someobj-none-in-python
        if not detail['responseElements']:
            logger.warning('Not responseElements found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False

        ec2 = boto3.resource('ec2')     #<- incijalizuje boto3 resurs

        #detail = event['detail']
        if eventname == 'CreateVolume':
            #The append() method adds a single item to the existing list. It doesn't return a new list; rather it modifies the original list.
            ids.append(detail['responseElements']['volumeId'])
            logger.info(ids)

        #eventname = detail['eventName']
        elif eventname == 'RunInstances':
            items = detail['responseElements']['instancesSet']['items']
            for item in items:
                ids.append(item['instanceId'])
            logger.info(ids)
            logger.info('number of instances: ' + str(len(ids)))
            #str() - Return a string version of object. If object is not provided, returns the empty string.
            #len() - Return the length (the number of items) of an object. 
            #The argument may be a sequence (such as a string, bytes, tuple, list, or range) or a collection (such as a dictionary, set, or frozen set).

            base = ec2.instances.filter(InstanceIds=ids)            <- filtrira po id instance, lista ids je pripremljena ranije
            #class EC2.Instance(id)
            #A resource representing an Amazon Elastic Compute Cloud (EC2) Instance:

            #ovo je python filter() f-ja
            #The filter() function returns an iterator were the items are filtered through a function to test if the item is accepted or not.

            #ovo je boto3 filter funkcija
            #filter(**kwargs)
            #Creates an iterable of all Volume resources in the collection filtered by kwargs passed to method.
            #https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html

            #loop through the instances
            for instance in base:
                #all() - Return True if all elements of the iterable are true (or if the iterable is empty).

                #https://stackoverflow.com/questions/37324085/boto3-get-ec2-instances-volume
                #volumes - A collection of Volume resources
                for vol in instance.volumes.all():          #<-base je lista svih instanci (filtrirana), vol je skup informacija o volume-u u okviru instance 
                    ids.append(vol.id)                      #na ids appendujemo id voluma

                #network_interfaces - A collection of NetworkInterface resources
                for eni in instance.network_interfaces:
                    ids.append(eni.id)                      #na ids appendujemo id network interface-a

                #print(ids)
                logger.info(ids)
                #rezultat:
                #['i-03e1539c01ed471a2', 'vol-05e64d41026d8ad1b', 'eni-045d14fe2fcdb5159']

        elif eventname == 'CreateImage':
            ids.append(detail['responseElements']['imageId'])
            logger.info(ids)

        elif eventname == 'CreateSnapshot':
            ids.append(detail['responseElements']['snapshotId'])
            logger.info(ids)
        else:
            logger.warning('Not supported action')

        #if condition:
        #  executeStatementBlock    
        #ids je lista koja postoji (true) i koja je popunjena (true) pa pretpostavljam da je condition true i 
        #for petlja (koja stampa obavestenja u CloudWatch log-u) i taguje instancu, volume i mrezni interfejs 
        if ids:
            for resourceid in ids:
                print('Tagging resource ' + resourceid)
            #create_tags(**kwargs)
            #Adds or overwrites one or more tags for the specified Amazon EC2 resource or resources. 
            #Each resource can have a maximum of 50 tags. Each tag consists of a key and optional value. 
            #Tag keys must be unique per resource.
            
            # Resources (list) --
            # [REQUIRED]

            # The IDs of one or more resources, separated by spaces.
            # (string) --
            
            # Tags (list) --
            # [REQUIRED]

            # One or more tags. The value parameter is required, 
            # but if you don't want the tag to have a value, specify the parameter with no value, 
            # and we set the value to an empty string.

            # (dict) --
            # Describes a tag.

            #     Key (string) --
            #     The key of the tag.
            #     Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws: .

            #     Value (string) --
            #     The value of the tag.
            #     Constraints: Tag values are case-sensitive and accept a maximum of 255 Unicode characters.

            ec2.create_tags(Resources=ids, Tags=[{'Key': 'Owner', 'Value': user}, {'Key': 'PrincipalId', 'Value': principal}, {'Key': 'Sloba', 'Value': 'car'}])

        logger.info(' Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        #https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
        #When Lambda runs your function, it passes a context object to the handler. 
        #This object provides methods and properties that provide information about the invocation, function, and execution environment.
        #get_remaining_time_in_millis – Returns the number of milliseconds left before the execution times out.
        return True
    #In Python 3.x, using as is required to assign an exception to a variable.
    except Exception as e:
        logger.error('Something went wrong: ' + str(e))0
        #exception dodeljen varijabli e, pretovern u string str(e) i poslat CloudWatch logu preko logger objekta 
        return False