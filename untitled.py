import boto3
import logging

logger = logging.getlogger()
#Loggers are never instantiated directly, 
#but always through the module-level function logging.getLogger(name). 

logger.setlevel(logging.INFO)
#setLevel(level)
#Sets the threshold for this logger to level. 
#Logging messages which are less severe than level will be ignored; 
