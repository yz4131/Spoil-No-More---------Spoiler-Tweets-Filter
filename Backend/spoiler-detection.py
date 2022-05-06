import boto3
import json
import os
from helper import one_hot_encode, vectorize_sequences
import numpy as np

# sagemaker endpoint
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

# sagemaker
sagemaker= boto3.client('runtime.sagemaker')

# retrive data from sqs
def get_data(queue_url):
    sqs = boto3.client('sqs')

    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return message

def lambda_handler(event, context):

    if event['queryStringParameters']['q'] == 'spoiler':
        # get data from sqs
        try:
            data = get_data('https://sqs.us-east-1.amazonaws.com/176363299110/tweets')
            data = data['MessageAttributes']['Tweets']['StringValue']
        except:
            res = {
            "isBase64Encoded": False,
            "statusCode": 404,
            "headers": {'Access-Control-Allow-Origin': '*'},
            "body": 'Not Found'
            }
            return res
        d = [str(data)]
        vocabulary_length = 9013
        one_hot_data = one_hot_encode(d, vocabulary_length)
        encoded_data = vectorize_sequences(one_hot_data, vocabulary_length)

        payload = json.dumps(encoded_data.tolist())
        # call sagemaker model endpoints
        response = sagemaker.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                           ContentType='application/json',
                                           Body=payload)

        result = json.loads(response['Body'].read().decode("utf-8"))
        pred = int(result['predicted_label'][0][0])
        score = result['predicted_probability'][0][0]
        label = pred
        response = {'data': data, 'labels': label}
        res = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Access-Control-Allow-Origin': '*'},
        "body": json.dumps(response)
        }
        return res

    elif event['queryStringParameters']['q'] == 'movie':
        spoil_words = ['moonknight', 'doctorstrange', 'spoiler', 'batman', 'moon',
        'team', 'knight', 'finale', 'avatar', 'marvel', 'halo', 'strange',
        'episode', 'lockley', 'multiverseofmadness', 'batman?rt', 'multiverse']

        try:
            data = get_data('https://sqs.us-east-1.amazonaws.com/176363299110/tweets')
            data = data['MessageAttributes']['Tweets']['StringValue']
        except:
            res = {
            "isBase64Encoded": False,
            "statusCode": 404,
            "headers": {'Access-Control-Allow-Origin': '*'},
            "body": 'Not Found'
            }
            return res

        label = 0

        for w in spoil_words:
            if w in data.lower():
                label = 1
                break

        response = {'data':data, 'labels': label}
        res = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Access-Control-Allow-Origin': '*'},
        "body": json.dumps(response)
        }
        return res
