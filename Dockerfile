FROM python:3.10

RUN mkdir /app
WORKDIR /app

# RUN apk --no-cache add musl-dev linux-headers g++

# RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY chatbot.py .
COPY lib ./lib

CMD ["python", "chatbot.py"]