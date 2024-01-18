FROM python:3.10-alpine

WORKDIR /library

COPY ./src/library_service /library
COPY ../config.yaml /library
COPY ../requirements.txt /library

RUN pip3.10 install -r requirements.txt

EXPOSE 8060

CMD ["python3", "app/main.py"]
