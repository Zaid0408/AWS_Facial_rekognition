import json
import boto3
import io
import uuid
import base64
# Function to test AWS rekognition and retrieve the predicted images of the user 
s3=boto3.client('s3')
rekognition=boto3.client('rekognition')

def lambda_handler(event, context):
    
    bucket_name = 'zaid-image-recog'
    folder_name='event1-imgs/'
    collection_id='event1-imgs'
    region='ap-south-1'
    
    
    body = json.loads(event['body'])
    image_data = body.get('image_data')
    
    decoded_image_data = base64.b64decode(image_data)
    # file_name = body.get('file_name')
    # Search the images having a given face in collection 
    try:
    
        predicted_faces = rekognition.search_faces_by_image(CollectionId=collection_id,Image={'Bytes':decoded_image_data},
            MaxFaces=4096 , # Number of face matches to return
            FaceMatchThreshold=90  # Minimum confidence level for the face match to return
        )
    except Exception as e:
        print('Error is',e)
        return {
            'statusCode': 500,
            'body': 'Error in searching Faces'
        }
        
    face_matches = predicted_faces['FaceMatches']
    
    presigned_urls = []
    for face in face_matches:
        image_id = face['Face']['ExternalImageId']
        object_key = f"{folder_name}{image_id}"
        presigned_url = s3.generate_presigned_url('get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=900  # URL expiry time in seconds (e.g., 1 hour)
        )
        presigned_urls.append(presigned_url)
    
    # Get no of entries in collection 
    # r = rekognition.list_faces(
    #         CollectionId=collection_id
    #     )
    # faces = r.get('Faces', [])
    # print(len(faces))
    # for face in faces:
    #     external_id=face['ExternalImageId']
    #     print(external_id)

    
        
    return {
        'statusCode': 200,
        'body': json.dumps(presigned_urls)
    }
    # try:
    #     rekognition.create_collection(CollectionId=collection_id)
    #     print(f'Creating new collection: {collection_id}')
    # except rekognition.exceptions.ResourceAlreadyExistsException:
    #     print(f'Collection {collection_id} already exists.\n')
    
    # List objects in the specified S3 folder
    # response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    
    # for obj in response.get('Contents', []):
    #     file_key = obj['Key']
    #     external_image_id=file_key.split('/')[-1]
    #     # print(external_image_id)
    #     if not file_key.endswith('/'):  # Ignore folder keys
    #         print(f'Processing file: {external_image_id}')
            
    #         # Index faces in the image
    #         try:
    #             response = rekognition.index_faces(
    #                 CollectionId=collection_id,
    #                 Image={'S3Object': {'Bucket': bucket_name, 'Name': file_key}},
    #                 DetectionAttributes=['ALL'],
    #                 ExternalImageId=external_image_id
    #             )
    #         except Exception as e:
    #             print(f'Error processing {file_key}: {str(e)}')
    
     

    
            
    # delete collection
    # res = rekognition.delete_collection(CollectionId=collection_id)
    # print(f'Successfully deleted collection: {collection_id}')
    # print('Response:', res)
    
    
    
    
       # delete image with external id in collection
    # response = rekognition.list_faces(
    #     CollectionId=collection_id,
    #     MaxResults=4096  # Adjust if you expect a large number of faces in the collection
    # )
    
    # face_id_to_delete = None
    # external_image_id = 'musk_test3.jpg'
    
    # # Find the FaceId corresponding to the ExternalImageId
    # for face in response['Faces']:
    #     if face['ExternalImageId'] == external_image_id:
    #         face_id_to_delete = face['FaceId']
    #         break
    
    # if face_id_to_delete:
    #     # Delete the face using FaceId
    #     delete_response = rekognition.delete_faces(
    #         CollectionId=collection_id,
    #         FaceIds=[face_id_to_delete]
    #     )
    #     print(f"Deleted face with FaceId: {face_id_to_delete}")
    