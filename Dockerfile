FROM crowdcoding/pcl-opencv-zbar

WORKDIR /src
COPY . .
RUN apt-get update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN pip install -r requirements.txt
CMD python3 app.py