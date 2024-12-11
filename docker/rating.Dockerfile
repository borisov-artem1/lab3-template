FROM python:3.10-alpine

WORKDIR /rating

COPY ./src/rating_service /rating
COPY ./config.yaml /rating
COPY ./requirements.txt /rating

RUN pip3.10 install -r requirements.txt

EXPOSE 8050

CMD ["python3", "app/main.py"]
