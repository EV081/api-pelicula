import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Inicializar datos para log
    log_data = {
        "tipo": "INFO",
        "log_datos": {}
    }
    
    try:
        # Entrada (json)
        log_data["log_datos"] = event
        print(json.dumps(log_data))  # Log json en CloudWatch
        
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        
        # Salida (json)
        log_data["log_datos"] = pelicula
        print(json.dumps(log_data))  # Log json en CloudWatch
        
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    
    except Exception as e:
        # Manejo de errores
        log_data["tipo"] = "ERROR"
        log_data["log_datos"] = {
            "error": str(e),
            "message": "Error al crear la película"
        }
        print(json.dumps(log_data))  # Log json de error en CloudWatch
        
        return {
            'statusCode': 500,
            'error': str(e),
            'message': "Ocurrió un error al procesar la solicitud"
        }
