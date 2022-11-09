import json
import boto3
import requests
import datetime

img_formats = ['jpg', 'jpeg', 'png']

def detect_labels(photo, bucket):
    
    client=boto3.client('rekognition', region_name = 'us-east-1')
    
    print('Start Labels Detecting')
    
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': photo
            }
        },
        MaxLabels=4
        )
    
    

    label_array = []
    for i in response['Labels']:
        label_array.append(i['Name'])
        
    print('Labels Detecting Done')
    
    return label_array
    

def headobject_retrieve(photo, bucket):
    
    s3=boto3.client('s3')
    
    print('Start Retrieving Head Object!')
    
    metadata_head = s3.head_object(
        Bucket = bucket,
        Key= photo
        )
        
    custom_label = metadata_head['Metadata']['customlabels'].split()
    
    print('Head Object Retrieving Done')
    
    return custom_label
    
def json_append(photo_label, custom_label, photo, bucket):
    
    print('Start Uploading Json!')
    
    url = 'https://search-photos-ehe7ivwsbhcxod3b27bmz763ti.us-east-1.es.amazonaws.com/photos/photos'
    headers = {"Content-Type": "application/json"}
    
    body = {
        "objectKey": photo, 
        "bucket": bucket,
        "createdTimestamp": str(datetime.datetime.now()),
        "labels": photo_label + custom_label
    }
    
    r = requests.post(url, data=json.dumps(body), auth = ('asm2master','Asm2master!'), headers=headers)
    
    print('Json Uploading Done:')


def lambda_handler(event, context):
    
    file_name = event['Records'][0]['s3']['object']['key']
    
    if not any(format in file_name.lower() for format in img_formats):
        print('Input object must be a jpg or png.')
        return {
          'statusCode': 422,
          'body' : json.dumps('Input object must be a jpg or png.')
        }
    else:
        photo = file_name
        bucket = event['Records'][0]['s3']['bucket']['name']
        photo_label=detect_labels(photo, bucket)
        custom_label = headobject_retrieve(photo, bucket)
        json_append(photo_label, custom_label, photo, bucket)
        
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
