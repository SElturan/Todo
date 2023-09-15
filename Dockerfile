FROM python:3.10

WORKDIR /app

COPY reguirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r reguirements.txt

COPY . .