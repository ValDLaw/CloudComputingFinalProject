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
- Añade los datos del SNS a la tabla en DynamoDB (usuario).

DynamoDB: usuario
- Contiene los registros de todos los usuarios.

### Revisar si el carnet ha vencido

EventBridge: RevisarCuenta
- Llama al Lambda (RevisarCuenta) cada día.

Lambda: RevisarCuenta
- Si el carnet universitario se ha vencido publica en SNS (TemaCarnetVencido).

SNS: TemaCarnetVencido
- Suscripciones:
    - SQS: ColaCarnetVencido

SQS: ColaCarnetVencido
- Suscripciones de SNS: TemaNuevaCuenta
- Desencadenadores de Lambda: ActualizarTarjeta

Lambda: ActualizarTarjeta
- Actualiza en la tabla en DynamoDB (usuario) el tipo de tarjeta de universitario a general en las tarjetas publicadas en SNS (TemaNuevaCuenta).