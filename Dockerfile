FROM zeburek/docker-python3-lxml-zbar

WORKDIR /src
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 app.py