import json
import boto3
from boto3.dynamodb.conditions import Key

def aprobado(dni, nombres):
    usuario = {
        'dni': dni,
        'nombres': nombres
    }
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:711711797456:TemaCuentaAprobada',
        Subject = 'Cuenta Aprobada',
        Message = json.dumps(usuario),
        MessageAttributes = {
            'dni': {'DataType': 'String', 'StringValue': dni },
            'nombres': {'DataType': 'String', 'StringValue': nombres }
        }
    )

def noAprobado(dni):
    temp = {'dni': dni}
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:711711797456:TemaCuentaAprobada',
        Subject = 'Cuenta No Aprobada',
        Message = json.dumps(temp),
        MessageAttributes = {
            'dni': {'DataType': 'String', 'StringValue': dni },
        }
    )


def lambda_handler(event, context):
    # Entrada (json)
    dni = event['dni']
    tipo = event['tipo']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    registros = dynamodb.Table('registro')

    if(tipo == 'Universitario'):
        responseT= registros.query(
            KeyConditionExpression=Key('tenant_id').eq('SUNEDU')
        )
    elif(tipo == 'Discapacitado'):
        responseT= registros.query(
            KeyConditionExpression=Key('tenant_id').eq('MINSA')
        )
    elif(tipo == 'General'):
        responseT= registros.query(
            KeyConditionExpression=Key('tenant_id').eq('RENIEC')
        )
        
    items = responseT['Items']
    
    respuesta = []
    for persona in items:
        if(persona['dni'] == dni):
            respuesta.append(registros.get_item(
                Key={'dni': dni}
            ))
            aprobado(persona['dni'], persona['nombres'])
        else:
            noAprobado(persona['dni'])    
            
    # Salida (json)
    return {
        'statusCode': 200,
        'response': respuesta
    } 