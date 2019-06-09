FROM python
WORKDIR /ReplicacaoDados
ADD . /ReplicacaoDados
RUN pip install -r requirements.txt
EXPOSE 5000
ENV NAME client
CMD ["python", "main.py", "localhost:5000", client]