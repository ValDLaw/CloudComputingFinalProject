import json
import boto3

def comparar_rostros(foto_uri):
    client = boto3.client('rekognition')
    response = client.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': 'nuevafoto',
                'Name': foto_uri
                }
            },
        TargetImage={
            'S3Object': {
                'Bucket': 'registrofoto',
                'Name': foto_uri
                }
            }
        
    )
    
    res = ""
    
    for record in response['FaceMatches']:
        face = record
        confidence=face['Face']
        if confidence['Confidence'] >= 95:
            res = "Aceptado."
        else:
            res = "Repetir."
        
        #print ("Matched With {}""%"" Similarity".format(face['Similarity']))
        #print ("With {}""%"" Confidence".format(confidence['Confidence']))
    
    for record in response['UnmatchedFaces']:
        res = "Denegado."
        #print ("No matched with {}""%"" Confidence".format(record['Confidence']))
    #print(response)
    
    return res


def lambda_handler(event, context):
    # Entrada (json), revisar en CloudWatch
    dni_uri = event['Records'][0]['s3']['object']['key']
    res = comparar_rostros(dni_uri)
    print(res)
    
    return {
        'statusCode': 200,
        'body': res
    }