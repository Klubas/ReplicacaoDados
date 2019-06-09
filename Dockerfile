FROM python
WORKDIR /ReplicacaoDados
ADD . /ReplicacaoDados
RUN pip install -r requirements.txt; docker pull mongo
EXPOSE 5000
ENV NAME server
CMD ["python", "main.py"]