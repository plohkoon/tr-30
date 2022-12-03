FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app

RUN apk --no-cache add musl-dev linux-headers g++

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py .
# COPY *.py lib ./

CMD ["python", "chatbot.py"]