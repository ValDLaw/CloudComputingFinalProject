import json
import random
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Entrada (json)
    # Funciona con EventBridge
    dynamodb = boto3.resource('dynamodb')
    recargas = dynamodb.Table('usuario')
    response_r = recargas.scan()
    items_r = response_r['Items']
    num_reg = response_r['Count'] - 1
    
    count = 0
    tarjeta_number = random.randint(0, num_reg)
    for item in items_r:
        if count == tarjeta_number:
            tenant_id = item['tenant_id']
            tarjeta_id = str(item['tarjeta_id'])
        count += 1
    
    recarga_id = str(random.randint(1, 999999999))
    monto = random.randint(1, 30) 
    #monto = event['monto']
    now = datetime.now()
    fecha_hora = str(now.date()) + "." + str(now.time())
    recarga = {
        'tenant_id': tenant_id,
        'recarga_id': recarga_id,
        'recarga_datos':{
            'tarjeta_id': tarjeta_id,
            'fecha_hora': fecha_hora,
            'monto': monto
        }
    }

    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
    	TopicArn = 'arn:aws:sns:us-east-1:021662273041:TemaNuevaRecarga',
    	Subject = 'Nueva Recarga',
        Message = json.dumps(recarga),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id },
            'recarga_id': {'DataType': 'String', 'StringValue': recarga_id },
            'tarjeta_id': {'DataType': 'String', 'StringValue': tarjeta_id },
            'monto': {'DataType': 'Number', 'StringValue': str(monto) }
        }
    )
    print(response_sns)    		
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response_sns
    }