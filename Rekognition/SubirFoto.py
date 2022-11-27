from __future__ import print_function
import boto3
import time, urllib
import json

#Función auxiliar para simular que se suben las fotos

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    # TODO implement
    dni = event['dni']
    image_name = event['image_name']
    copy_source = {
        'Bucket': 'localfoto',
        'Key': image_name
    }
    response = s3.meta.client.copy(copy_source, 'nuevafoto', dni + '.jpg')
    
    return {
        'statusCode': 200,
        'body': response
    }