FROM crowdcoding/pcl-opencv-zbar

WORKDIR /src
RUN apt-get update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python3 app.py