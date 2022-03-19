import os
import wmi
import datetime as dt
import boto3
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
temperature_infos = w.Sensor()
tempDict = {}
for sensor in temperature_infos:
    if sensor.SensorType==u'Temperature':
        tempDict[sensor.Name]=sensor.value
       
#print(tempDict)
        



#time_now = dt.datetime.utcnow()
#print(time_now)


event_time = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)

#print(event_time)



message = 'gpu ' + str(tempDict['GPU Core']) + ' cpu ' + str(tempDict['CPU Package'])
print(message)
#print(len(str(message)))
#print(str(message))



cw_client = boto3.client('logs'
 ,aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID']
     ,aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
     ,region_name=os.environ['AWS_DEFAULT_REGION'])

response = cw_client.describe_log_streams(logGroupName='/ferrell/brayden', logStreamNamePrefix='pc_temperature')
sequenceToken = response['logStreams'][0]['uploadSequenceToken']
#print(sequenceToken)
response = cw_client.put_log_events(
    logGroupName='/ferrell/brayden'
    ,logStreamName='pc_temperature'
    ,sequenceToken = sequenceToken
    ,logEvents=[
        {
            'timestamp': event_time
            ,'message': str(message)
        }
    ]
)
 

#print(response)
if sequenceToken == response['nextSequenceToken']:
    print('failed')
else:
    print('success')
