from tweepy import Stream
import json
import time
import boto3


class TweetsListener(Stream):
    def __init__(self,*args):
        super().__init__(*args)

    def on_data(self, data):
        session = boto3.Session(
            aws_access_key_id='',
            aws_secret_access_key=''
        )
        sqs = session.client('sqs', region_name='us-east-1')
        try:
            time.sleep(2)
            msg = json.loads(data)
            print('TWEETS:{}\n'.format(msg['text']))
            response = sqs.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/176363299110/streaming',
                DelaySeconds=1,
                MessageAttributes={
                    'Tweets': {
                        'DataType': 'String',
                        'StringValue': msg['text']
                    }
                },
                MessageBody=(
                    'Streaming.'
                )
            )
            print(response['MessageId'])
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)
        return False

    
def getData(tags):
    ACCESS_TOKEN = ''
    ACCESS_SECRET = ''
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    twitter_stream = TweetsListener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    twitter_stream = twitter_stream.filter(track=tags,languages=['en'])


class twitter_client:
    def run_client(self, tags):
        while True:
          getData(tags)


if __name__ == '__main__':
    tags = ['#Moon Knight', 'Moon Knight', 'MoonKnight', 'Batman', 'Morbius']
    client = twitter_client()
    client.run_client(tags)