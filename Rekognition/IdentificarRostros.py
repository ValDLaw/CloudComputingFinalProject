import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('rekognition')
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': 'nuevousuario',
                'Name': 'lisa2.jpeg'
                }
            },
        TargetImage={
            'S3Object': {
                'Bucket': 'nuevousuario',
                'Name': 'jisoo1.jpg'
                }
            } #'Name': 'marvinskynaruto.png'
        
    )
    for record in response['FaceMatches']:
        face = record
        confidence=face['Face']
        print ("Matched With {}""%"" Similarity".format(face['Similarity']))
        print ("With {}""%"" Confidence".format(confidence['Confidence']))
    
    for record in response['UnmatchedFaces']:
        print ("No matched with {}""%"" Confidence".format(record['Confidence']))
    #print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }