import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    key_to_update = json.loads(body['Message'])
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('usuario')
    
    response = table.update_item(
        Key={
            'tenant_id': key_to_update['tenant_id'],
            'tarjeta_id': int(key_to_update['tarjeta_id']),
        },
        UpdateExpression="set tipo=:tipo",
        ExpressionAttributeValues={
            ':tipo': 'general'
        },
        ReturnValues="UPDATED_NEW"
    )

    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
    
