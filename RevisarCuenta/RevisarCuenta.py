import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    Message = json.loads(body['Message'])
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('proceso')
    registros = dynamodb.Table('registro')
    user = {
        'tenant_id' : Message['tenant_id'],
        'dni': Message['dni'],
        'tipo': Message['tipo']
    }
    
    print(user)

    if(user['tipo'] == 'universitario'):
        responseT= registros.query(
        KeyConditionExpression=Key('tenant_id').eq('SUNEDU')
    )
    elif(user['tipo'] == 'discapacitado'):
        responseT= registros.query(
        KeyConditionExpression=Key('tenant_id').eq('MINSA')
    )
    elif(user['tipo'] == 'general'):
        responseT= registros.query(
        KeyConditionExpression=Key('tenant_id').eq('RENIEC')
    )
    items = responseT['Items']
    
    response = ""
    
    #respuesta = [{'records': 'hola'}]
    for persona in items:
        if(persona['dni'] == user['dni']):
            print("Aprobado.")
            updated = table.update_item(
                Key={
                    'tenant_id': user['tenant_id'],
                    'dni': user['dni'],
                },
                UpdateExpression="set revisarcuenta=:revisarcuenta",
                ExpressionAttributeValues={
                    ':revisarcuenta': 'Aprobado' #pasar fase 1
                },
                ReturnValues="UPDATED_NEW"
            )

            response = registros.get_item(
                Key={
                    'tenant_id' : user['tenant_id'],
                    'dni': user['dni']
                }
            )
        else:
            updated = table.update_item(
                Key={
                    'tenant_id': user['tenant_id'],
                    'dni': user['dni'],
                },
                UpdateExpression="set revisarcuenta=:revisarcuenta",
                ExpressionAttributeValues={
                    ':revisarcuenta': 'Denegado' #pasar fase 1
                },
                ReturnValues="UPDATED_NEW"
            )
            print("Denegado.")

            
    # Salida (json)
    #print(response)
    return {
        'statusCode': 200,
        'response': response
    }