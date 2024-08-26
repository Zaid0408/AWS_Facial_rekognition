import json
import boto3
import os
s3=boto3.client('s3')
rekognition=boto3.client('rekognition')
# Function will get triggered when one uploads an image to an s3 bucket. Will then upload the image to the AWS rekognition collection
def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    collection_id='event1-imgs'
    external_image_id=file_key.split('/')[-1]
    
    #  Index faces in the image
    try:
        response = rekognition.index_faces(CollectionId=collection_id,Image={'S3Object': {'Bucket': bucket_name, 'Name': file_key}},
                    DetectionAttributes=['ALL'],ExternalImageId=external_image_id
        )
        # print(response)
        print('Success in moving image to collection')
    except Exception as e:
        print(f'Error processing {file_key}: {str(e)}')
        
        
    
    r = rekognition.list_faces(CollectionId=collection_id)
    faces = r.get('Faces', [])
    print(len(faces))
    
    # print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Image indexing complete.')
    }
    
    # sort this code this try catch not needed
    # try:
    #     rekognition.create_collection(CollectionId=collection_id)
    #     print(f'Creating new collection: {collection_id}')
    # except rekognition.exceptions.ResourceAlreadyExistsException:
    #     print(f'Collection {collection_id} already exists.')
