# Comunicação entre duas aplicações cliente servidor 

## Cliente
 - Recebe os dados
 - Envia para o servidor
 
## Servidor
 - Recebe os dados do cliente
 - Salva os dados do cliente 
 - Replica os dados no cliente

### Configurações
    
    ~/.aws/config

        [default]
        access_key=
        secret_key=
        region=sa-east-1

## Build

* Server

        docker build -f Dockerfile-server -t replicacao-dados-server
 
* Client
        
        docker build -f Dockerfile-client -t replicacao-dados-client

## Run

* Server
        
        docker run -p 5000:5000 replicacado-dados-server
    
* Client
        
        docker run -p 5000:5000 replicacao-dados-client
    
 
## Referências

- https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

- https://medium.com/grupy-rn/trabalhando-com-python-e-mongodb-1d23ee042658

- https://flask-restful.readthedocs.io/en/latest/quickstart.html

- https://hackernoon.com/publish-your-docker-image-to-docker-hub-10b826793faf