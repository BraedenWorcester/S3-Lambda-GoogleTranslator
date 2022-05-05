import json
import urllib.parse
import boto3
from google_trans_new import google_translator 
t = google_translator()
s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        if (key.split('.')[-1] != 'txt'):
                print("failed translating '" + key + "' in '" + bucket + "': file must be of type '.txt'")
                return -1
    except IndexError as e:
        print("failed translating '" + key + "' in '" + bucket + "': file must be of type '.txt'")
        return -1
    try:
        if (key.split('/')[-2].lower() == 'translated'):
            print("failed translating '" + key + "' in '" + bucket + "': will not translate files in directory named 'translated' to avoid recursion")
            return -1
    except IndexError as e:
        print(e)
    try:
        resource = s3.get_object(Bucket=bucket, Key=key)
        translated = ""
        for line in resource['Body'].iter_lines():
            translated = translated + t.translate(line.decode('utf-8'), lang_tgt='en') + "\n"
        if (len(key.split('/')) == 1):
            s3.put_object(Bucket=bucket, Key= '/'.join(key.split('/')[0:-1]) + "translated/" + key.split('/')[-1], Body=translated)
        else:
            s3.put_object(Bucket=bucket, Key= '/'.join(key.split('/')[0:-1]) + "/translated/" + key.split('/')[-1], Body=translated)
        print("successfully translated '" + key + "' in '" + bucket + "'")
        return 1
    except Exception as e:
        print("failed translating '" + key + "' in '" + bucket + "': " + e)
        raise e
