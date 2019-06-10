#!/usr/bin/env bash

docker login

docker build -f Dockerfile-server -t replicacao-dados-server ./ && docker tag replicacao-dados-server klubas/replicacao:server

docker build -f Dockerfile-client -t replicacao-dados-client ./ && docker tag replicacao-dados-client klubas/replicacao:client

docker push klubas/replicacao:server && docker push klubas/replicacao:client

# docker run -it -p 5000:5000 klubas/replicacao:server

# docker run -it -p 5000:5000 klubas/replicacao:client
