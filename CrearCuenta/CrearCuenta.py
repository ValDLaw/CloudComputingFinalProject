import json
import boto3
    
    
def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    Message = json.loads(body['Message'])
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('usuario')
    user = {
        'tenant_id': Message['tenant_id'],
        'tarjeta_id': Message['tarjeta_id'],
        'dni': Message['dni'],
        'tipo': Message['tipo'],
        'cuenta': Message['cuenta']
    }
    print(user) # Revisar en CloudWatch
    response = table.put_item(Item=user)
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
