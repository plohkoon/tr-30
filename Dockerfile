FROM python:3.10

RUN mkdir /app
WORKDIR /app

# RUN apk --no-cache add musl-dev linux-headers g++

# RUN pip install --upgrade pip setuptools wheel

RUN apt-get update && \
  apt-get install -y texlive-latex-base texlive-latex-extra texlive-extra-utils poppler-utils pnmtopng

RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY chatbot.py test.py ./
COPY lib ./lib

CMD ["python", "chatbot.py"]