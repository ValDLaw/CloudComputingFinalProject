# CloudComputingFinalProject

## Nueva Cuenta

### Colocar cuenta en la tabla

Lambda: Nueva Cuenta
- Obtiene los datos del potencial usuario
- Publica en SNS (TemaNuevaCuenta)

SNS: TemaNuevaCuenta
- Suscripciones:
    - SQS: ColaCrearCuenta

SQS: ColaCrearCuenta
- Suscripciones de SNS: TemaNuevaCuenta
- Desencadenadores de Lambda: CrearCuenta

Lambda: CrearCuenta
- Añade los datos del SNS a la tabla en DynamoDB (usuario)

DynamoDB: usuario
- Contiene los registros de todos los usuarios.
