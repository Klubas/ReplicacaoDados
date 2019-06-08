FROM python
WORKDIR /ReplicacaoDados
ADD . /ReplicacaoDados
RUN pip install -r requirements.txt
EXPOSE 5000
ENV NAME world
CMD ["python", "main.py", "client", "replicacaodados.herokuapp.com:5000"]