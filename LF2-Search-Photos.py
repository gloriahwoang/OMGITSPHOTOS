import json
import datetime
import time
import os
import dateutil.parser
import logging
import boto3
import re
import requests
from requests_aws4auth import AWS4Auth


def FindPhotofromOpenSearch(labels):
    
    client = boto3.client('s3')
    
    region = 'us-east-1'
    service = 'es'
    
    # credentials = boto3.Session().get_credentials()
    # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    host = 'https://search-photos-ehe7ivwsbhcxod3b27bmz763ti.us-east-1.es.amazonaws.com'
    index = 'photos'
    url = host + '/' + index + '/_search'
    print('step1')
    headers = { "Content-Type": "application/json" }
    
    photos = []
    location = []
    
    if len(labels) == 2 and labels[1][-1] == 's':
        labels.append(labels[1][:-1])
        
    if labels[0][-1] == 's':
        labels.append(labels[0][:-1])
    
    for i in range(len(labels)):
        query = {
            "query": {
                "multi_match": {
                    "query": labels[i],
                }
            }
        }
        print('step2 query: ', query)
        
        response = requests.get(url, data=json.dumps(query), auth = ('asm2master','Asm2master!'), headers=headers)
        print('step3 response: ', response)
        res = response.json()
        print('step4 res: ', res)
        noOfHits = res['hits']['total']
        
        hits = res['hits']['hits']
        print('step5 : ', hits)
        
        # https://asm2.s3.amazonaws.com/jujutsukaisen.jpeg
        for hit in hits:
            photos.append('https://asm2.s3.amazonaws.com/'+ str(hit['_source']['objectKey']))
            # response = client.get_object(
            #     Bucket=str(hit['_source']['bucket']),
            #     Key=str(hit['_source']['objectKey'])
            #     )
                
        # print('response:', response)
        print('step7 photos: ', photos)
        # print('step8 location: ', location)
    
    return photos    
    # return photos, location

def get_response(code, body):
    response = {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT',
            'Access-Control-Allow-Headers': '*'
            
        },
        'body': json.dumps(body),
        'isBase64Encoded': False
    }
    print('get_response:', response)
    return response



def lambda_handler(event, context):
    # By default, treat the user request as coming from the EST time zone.
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()
    
    client = boto3.client('lexv2-runtime')
    print('event: ', event)
    msg_from_usr = json.dumps(event['multiValueQueryStringParameters']['q'][0])
    response = client.recognize_text(botId='GN0FREQNKZ',botAliasId='THSR06QIAM',localeId='en_US',sessionId='testuser',text=msg_from_usr)
    print('response:', response)
    
    label1_msg_from_lex = response['interpretations'][0]['intent']['slots']['labels1']['value']['resolvedValues'][0]
    
    if response['interpretations'][0]['intent']['slots']['labels2'] is None:
        search_label = [label1_msg_from_lex]
    else:
        label2_msg_from_lex = response['interpretations'][0]['intent']['slots']['labels2']['value']['resolvedValues'][0]
        search_label = [label1_msg_from_lex, label2_msg_from_lex]
    
    print('search_label: ', search_label)
    
    hehehaha= FindPhotofromOpenSearch(search_label)
    
    
    
    
    if len(hehehaha) != 0:
        print(hehehaha, len(hehehaha))
        return get_response(200, hehehaha)
    else:
        return {
        'statusCode': 200,
        'body': json.dumps('Nothing Found')
    }
    
    
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
