import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    tarjeta_id = event['tarjeta_id']
    tipo = event['tipo']
    dni = event['dni']
    cuenta = event['cuenta']
    usuario = {
        'tenant_id': tenant_id,
        'tarjeta_id': tarjeta_id,
        'tipo': tipo,
        'dni': dni,
        'cuenta': cuenta
    }
    
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:021662273041:TemaNuevaCuenta',
        Subject = 'Nueva Cuenta',
        Message = json.dumps(usuario),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id }
        }
    )    
    # TODO implement
    return {
        'statusCode': 200,
        'body': response_sns
    }