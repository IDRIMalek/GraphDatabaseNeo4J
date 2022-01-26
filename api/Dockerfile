FROM debian:latest
ADD . /home
WORKDIR /home
RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt
EXPOSE 8000
CMD  uvicorn api:app --host 0.0.0.0 --port 8000 
#malekidri/api_projet3