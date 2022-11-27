import json
import boto3

def getdni(foto_uri):
    flag = False
    dni = ""
    for c in foto_uri:
        if flag:
            dni += c
        if c == "_":
            flag = True
    
    return dni
    
def gettenant_id(foto_uri):
    tenant_id = ""
    for c in foto_uri:
        if c == "_":
            break
        tenant_id += c
    
    return tenant_id

def comparar_rostros(foto_uri):
    dnijpg = getdni(foto_uri)
    tenant_id = gettenant_id(foto_uri)
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
                'Name': dnijpg
                }
            }
        
    )
    
    res = ""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('proceso')
    
    for record in response['FaceMatches']:
        face = record
        confidence=face['Face']
        if confidence['Confidence'] >= 95:
            updated = table.update_item(
                Key={
                    'tenant_id': tenant_id,
                    'dni': dnijpg[:-4],
                },
                UpdateExpression="set identificarfoto=:identificarfoto",
                ExpressionAttributeValues={
                    ':identificarfoto': 'Aprobado' #pasar fase 1
                },
                ReturnValues="UPDATED_NEW"
            )
            res = "Aprobado."
        
        #print ("Matched With {}""%"" Similarity".format(face['Similarity']))
        #print ("With {}""%"" Confidence".format(confidence['Confidence']))
    
    for record in response['UnmatchedFaces']:
        updated = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'dni': dnijpg[:-4],
            },
            UpdateExpression="set identificarfoto=:identificarfoto",
            ExpressionAttributeValues={
                ':identificarfoto': 'Denegado' #pasar fase 1
            },
            ReturnValues="UPDATED_NEW"
        )
        res = "Denegado."
        #print ("No matched with {}""%"" Confidence".format(record['Confidence']))
    #print(response)
    
    return res


def lambda_handler(event, context):
    # Entrada (json), revisar en CloudWatch
    foto_uri = event['Records'][0]['s3']['object']['key']
    res = comparar_rostros(foto_uri)
    print(res)
    
    return {
        'statusCode': 200,
        'body': res
    }