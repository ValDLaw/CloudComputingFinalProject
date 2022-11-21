import json
import random
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key

def check(tenant_id, tarjeta_id, fecha_ven, hoy):
    # TODO implement
    
    key_to_update = {
        'tenant_id': tenant_id,
        'tarjeta_id': int(tarjeta_id)
    }
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:021662273041:TemaCarnetVencido',
        Subject = 'Check Date',
        Message = json.dumps(key_to_update),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id },
            'tarjeta_id': {'DataType': 'Number', 'StringValue': tarjeta_id }
        }
    )

    return key_to_update


def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    usuario = dynamodb.Table('usuario')
    response_u = usuario.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    items_u = response_u['Items']
    
    
    registros = dynamodb.Table('registros')
    response_r = registros.query(
        KeyConditionExpression=Key('tenant_id').eq('SUNEDU')
    )
    items_r = response_r['Items']
    
    fecha_ven = ''
    items = []
    
    for user in items_u:
        if user['tipo'] == "universitario":
            for reg in items_r: #que coincidan fecha y usuarios
                if user['dni'] == reg['dni']:
                    fecha_ven = reg['fecha_ven']
                    now = datetime.now()
                    now = now - timedelta(hours=5) #UTC-5
                    hoy = str(now.date())
                    if hoy == fecha_ven: #si vence hoy
                        key_to_update = check(tenant_id, str(user['tarjeta_id']), fecha_ven, hoy)
                        items.append(key_to_update)

    # Salida (json)
    return {
        'statusCode': 200,
        'body': items
    }