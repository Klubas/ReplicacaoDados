# Comunicação entre duas aplicações cliente servidor 

## Cliente
 - Recebe os dados
 - Envia para o servidor
 
## Servidor
 - Recebe os dados do cliente
 - Salva os dados do cliente 
 - Replica os dados no cliente

### Dependências
- boto3
- flask

### Configurações
    
    ~/.aws/config

        [default]
        access_key=
        secret_key=
        region=sa-east-1
 
## Referências

- https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html