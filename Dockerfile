FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3 python3-pip

COPY . .

RUN pip3 install -r requirements.txt


EXPOSE 5000


ENTRYPOINT ["python3"]
CMD ["app.py"]