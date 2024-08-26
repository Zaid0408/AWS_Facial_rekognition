import json
import boto3
import base64
# Upload image to a folder in an  s3 bucket
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket_name = 'zaid-image-recog'
    folder_path = 'event1-imgs'
    body = json.loads(event['body'])
    image_data = body.get('image_data')
    file_name=body.get('file_name')
    unique_key = f'{folder_path}/{file_name}'
    print(f'\n{unique_key}')
    
    print(file_name)
    
    # Decode the base64 image data
    decoded_image_data = base64.b64decode(image_data)
   
    s3_client.put_object(
        Bucket=bucket_name,
        Key=unique_key,
        Body=decoded_image_data,
        ContentType=f'image/jpg'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Image uploaded successfully to {bucket_name} and has key value {unique_key}!')
    }
