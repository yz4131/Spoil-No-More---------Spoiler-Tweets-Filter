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
    # call sagemaker model endpoints
    # data = get_data('https://sqs.us-east-1.amazonaws.com/176363299110/streaming')
    data = ["""In its Oscar year, Shawshank Redemption (written and directed by Frank Darabont, after the novella Rita Hayworth and the Shawshank Redemption, by Stephen King) was nominated for seven Academy Awards, and walked away with zero. Best Picture went to Forrest Gump, while Shawshank and Pulp Fiction were "just happy to be nominated." Of course hindsight is 20/20, but while history looks back on Gump as a good film, Pulp and Redemption are remembered as some of the all-time best. Pulp, however, was a success from the word "go," making a huge splash at Cannes and making its writer-director an American master after only two films. For Andy Dufresne and Co., success didn't come easy. Fortunately, failure wasn't a life sentence.After opening on 33 screens with take of $727,327, the $25M film fell fast from theatres and finished with a mere $28.3M. The reasons for failure are many. Firstly, the title is a clunker. While iconic to fans today, in 1994, people knew not and cared not what a 'Shawshank' was. On the DVD, Tim Robbins laughs recounting fans congratulating him on "that 'Rickshaw' movie." Marketing-wise, the film's a nightmare, as 'prison drama' is a tough sell to women, and the story of love between two best friends doesn't spell winner to men. Worst of all, the movie is slow as molasses. As Desson Thomson writes for the Washington Post, "it wanders down subplots at every opportunity and ignores an abundance of narrative exit points before settling on its finale." But it is these same weaknesses that make the film so strong.Firstly, its setting. The opening aerial shots of the prison are a total eye-opener. This is an amazing piece of architecture, strong and Gothic in design. Immediately, the prison becomes a character. It casts its shadow over most of the film, its tall stone walls stretching above every shot. It towers over the men it contains, blotting out all memories of the outside world. Only Andy (Robbins) holds onto hope. It's in music, it's in the sandy beaches of Zihuatanejo; "In here's where you need it most," he says. "You need it so you don't forget. Forget that there are places in the world that aren't made out of stone. That there's a - there's a - there's something inside that's yours, that they can't touch." Red (Morgan Freeman) doesn't think much of Andy at first, picking "that tall glass o' milk with the silver spoon up his ass" as the first new fish to crack. Andy says not a word, and losing his bet, Red resents him for it. But over time, as the two get to know each other, they quickly become the best of friends. This again, is one of the film's major strengths. Many movies are about love, many flicks have a side-kick to the hero, but Shawshank is the only one I can think of that looks honestly at the love between two best friends. It seems odd that Hollywood would skip this relationship time and again, when it's a feeling that weighs so much into everyone's day to day lives. Perhaps it's too sentimental to seem conventional, but Shawshank's core friendship hits all the right notes, and the film is much better for it.It's pacing is deliberate as well. As we spend the film watching the same actors, it is easy to forget that the movie's timeline spans well over 20 years. Such a huge measure of time would pass slowly in reality, and would only be amplified in prison. And it's not as if the film lacks interest in these moments. It still knows where it's going, it merely intends on taking its sweet time getting there. It pays off as well, as the tedium of prison life makes the climax that much more exhilarating. For anyone who sees it, it is a moment never to be forgotten.With themes of faith and hope, there is a definite religious subtext to be found here. Quiet, selfless and carefree, Andy is an obvious Christ figure. Warden Norton (Bob Gunton) is obviously modeled on Richard Nixon, who, in his day, was as close to a personified Satan as they come. But if you aren't looking for subtexts, the movie speaks to anyone in search of hope. It is a compelling drama, and a very moving film, perfectly written, acted and shot. They just don't come much better than this.OVERALL SCORE: 9.8/10 = A+ The Shawshank Redemption served as a message of hope to Hollywood as well. More than any film in memory, it proved there is life after box office. Besting Forrest and Fiction, it ran solely on strong word of mouth and became the hottest rented film of 1995. It currently sits at #2 in the IMDb's Top 250 Films, occasionally swapping spots with The Godfather as the top ranked film of all time -- redemption indeed. If you haven't seen it yet, what the hell are you waiting for? As Andy says, "It comes down a simple choice, really. Either get busy living, or get busy dying."""]
    vocabulary_length = 9013
    one_hot_data = one_hot_encode(data, vocabulary_length)
    encoded_data = vectorize_sequences(one_hot_data, vocabulary_length)

    payload = json.dumps(encoded_data.tolist())
    response = sagemaker.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=payload)

    result = json.loads(response['Body'].read().decode("utf-8"))
    pred = int(result['predicted_label'][0][0])
    score = result['predicted_probability'][0][0]
    label = 'Spoiler' if pred == 1 else 'non-spoiler'
    print(label)
