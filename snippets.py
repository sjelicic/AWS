#Basic import boto3 libraries
import boto3
import sys

#provided Access Credentialsaccess_key
access_key = ""
secret_key = ""

count=0
#Establish a connection to EC2 resource using credentials and region_name
conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,region_name='us-west-1')
print("Argument length: ",len(sys.argv))

if len(sys.argv)>2:
    Keyname = sys.argv[1]
    value = sys.argv[2]
    instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped'],'Name': 'tag:'+Keyname,'Values': [value]}])
    print("Arguments passed\nKey: "+Keyname+"\nValue: "+value)
else:
    instances = conn.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])

for instance in instances:
    #instance.start(instance.id)
    count+=1
    print(instance.id,",",instance.state["Name"])

print("Total number of EC2 instances are stopped on cloud: ",count)