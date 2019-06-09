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
        
## Uso

* Run server
        
        docker run replicacado-dados-server
    
* Run client
        
        docker run replicacao-dados-client
    
 
## Referências

- https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

- https://medium.com/grupy-rn/trabalhando-com-python-e-mongodb-1d23ee042658