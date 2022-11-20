import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    print(event) # Revisar en CloudWatch
    body = json.loads(event['Records'][0]['body'])
    recarga_json = json.loads(body['Message'])
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('recargas_t')
    
    #print(recarga) -> Revisar en CloudWatch
    response = table.put_item(Item=recarga_json)
    
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }