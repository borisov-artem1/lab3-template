FROM python:3.10-alpine

WORKDIR /reservation

COPY ./src/reservation_service /reservation
COPY ../config.yaml /reservation
COPY ../requirements.txt /reservation

RUN pip3.10 install -r requirements.txt

EXPOSE 8070

CMD ["python3", "app/main.py"]
