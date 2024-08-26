import json
import boto3
import io

# Function to delete image from collection and s3 bucket
s3=boto3.client('s3')
rekognition=boto3.client('rekognition')

def lambda_handler(event, context):
    # TODO implement
    # print(event)
    
    bucket_name = 'zaid-image-recog'
    folder_name='event1-imgs/'
    
    collection_id='event1-imgs'
    region='ap-south-1'
    body = json.loads(event['body'])
    file_key = file_name=body.get('file_name')
    object_key=f'{folder_name}{file_key}'
    
       # delete image with external id in collection
    response = rekognition.list_faces(
        CollectionId=collection_id,
        MaxResults=4096  # Adjust if you expect a large number of faces in the collection
    )
    
    face_id_to_delete = None
    
    # Find the FaceId corresponding to the ExternalImageId which is file_key in this case
    for face in response['Faces']:
        if face['ExternalImageId'] == file_key:
            face_id_to_delete = face['FaceId']
            break
     # Delete the face using FaceId
    if face_id_to_delete is None:
        return {
            'statusCode': 404,
            'body': json.dumps('Image does not exist in the collection! ')
        }
        
    else:

        delete_response = rekognition.delete_faces(
            CollectionId=collection_id,
            FaceIds=[face_id_to_delete]
        )
        print(f"Deleted face with FaceId: {face_id_to_delete}")
        
        # delete from s3 bucket 
        try:
            response = s3.delete_object(Bucket=bucket_name, Key=object_key)
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Delete face from collection but Error deleting image from s3 bucket : {str(e)}'
            }
    
    response_body=f'Deleted face with name {file_key} from collection and S3 bucket.'
    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }
    
    
    
    
