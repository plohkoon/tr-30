FROM alpine:latest AS build-simc

ARG THREADS=1
ARG PGO_PROFILE="CI.simc"
ARG GITHUB_URL="https://github.com/simulationcraft/simc"

RUN apk --no-cache add --virtual build_dependencies \
        compiler-rt \
        curl-dev \
        clang-dev \
        llvm \
        g++ \
        make \
        git

RUN echo "Cloning SimulationCraft repository" && \
    git clone --depth 1 ${GITHUB_URL} /simc/ && \
    cd /simc/ && \
    git submodule update --init --recursive
WORKDIR /simc/

RUN cd /simc/engine && \
    make optimized

FROM python:3.10.15-alpine3.20

RUN mkdir /app
WORKDIR /app

RUN apk update && \
    apk --no-cache add --virtual build_dependencies \
        libcurl \
        libgcc \
        libstdc++ \
        texlive \
        # TODO - Try to reduce this to just standalone
        texlive-most \
        texlive-xetex \
        poppler-utils \
        netpbm \
        imagemagick

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY --from=build-simc /simc/engine/simc /bin/simc

COPY chatbot.py chatbot.py
COPY lib ./lib

CMD ["python", "chatbot.py"]
