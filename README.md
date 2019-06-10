# Comunicação e replicação entre duas aplicações e bancos de dados não relacionais

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
        
    cd path/to/ReplicacadoDados
        
    docker build -f Dockerfile-server -t replicacao-dados-server ./
 
    docker build -f Dockerfile-client -t replicacao-dados-client ./
        
## Tag e Push
    
    docker tag replicacao-dados-server klubas/replicacao:server
    
    docker tag replicacao-dados-client klubas/replicacao:client
    
    docker push klubas/replicacao:server

    docker push klubas/replicacao:client

## Run

* Server
        
        docker pull klubas/replicacao:server
    
        docker run -it -p 5000:5000 klubas/replicacao:server
    
* Client

        docker pull klubas/replicacao:client
        
        docker run -it -p 5000:5000 klubas/replicacao:client
    
## Referências

- https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html

- https://medium.com/grupy-rn/trabalhando-com-python-e-mongodb-1d23ee042658

- https://flask-restful.readthedocs.io/en/latest/quickstart.html

- https://hackernoon.com/publish-your-docker-image-to-docker-hub-10b826793faf