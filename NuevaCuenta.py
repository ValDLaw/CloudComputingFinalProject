from __future__ import print_function
import json
import boto3
import time, urllib
import uuid
from boto3.dynamodb.conditions import Key

def subirfoto(tenant_id, dni, image_name):
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': 'localfoto',
        'Key': image_name
    }
    name = tenant_id + '_' + dni + '.jpg'
    response = s3.meta.client.copy(copy_source, 'nuevafoto', name)

def revisarcuenta(usuario):
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:021662273041:TemaRevisarCuenta',
        Subject = 'Revisión de cuenta',
        Message = json.dumps(usuario),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': usuario['tenant_id'] }
        }
    )

def crearcuenta(usuario):
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:021662273041:TemaNuevaCuenta',
        Subject = 'Nueva Cuenta',
        Message = json.dumps(usuario),
        MessageAttributes = {
        'tenant_id': {'DataType': 'String', 'StringValue': usuario['tenant_id'] }
        }
    )  

def query_proceso(table, tenant_id, dni):
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    items = response['Items']
    
    for p in items:
        if p['dni'] == dni:
            return p

def lambda_handler(event, context):
    tenant_id = event['tenant_id']
    tarjeta_id = str(uuid.uuid1())
    tipo = event['tipo']
    dni = event['dni']
    cuenta = event['cuenta']
    saldo = 0
    image_name = event['image_name']
    
    usuario = {
        'tenant_id': tenant_id,
        'tarjeta_id': tarjeta_id,
        'tipo': tipo,
        'dni': dni,
        'cuenta': cuenta,
        'saldo': saldo
    }
    
    #Crear proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('proceso')
    proceso_id = str(uuid.uuid1())
    proceso = {
        'tenant_id': tenant_id,
        'dni': dni,
        'identificarfoto': "-",
        'revisarcuenta': "-"
    }
    table.put_item(Item=proceso)
    
    subirfoto(tenant_id, dni, image_name) #rekognition, comparar fotos
    revisarcuenta(usuario)
    crearcuenta(usuario)
    
    return {
        'statusCode': 200,
        'body': usuario
    }
    