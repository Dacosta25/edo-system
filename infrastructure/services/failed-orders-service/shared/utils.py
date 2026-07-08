import json

def parse_sqs_event(event):
    for record in event['Records']:
        body = json.loads(record['body'])
        yield json.loads(body['Message'])
