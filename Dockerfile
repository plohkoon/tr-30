# FROM alpine:latest AS build-simc

# ARG THREADS=1
# ARG APIKEY=""
# ARG PGO_PROFILE="CI.simc"

# RUN apk --no-cache add --virtual build_dependencies \
#         compiler-rt \
#         curl-dev \
#         clang-dev \
#         llvm \
#         g++ \
#         make \
#         git

# RUN mkdir -p /app/ && \
#     cd /app/ && \
#     git clone https://github.com/simulationcraft/simc

# RUN echo "Building simc executable" && \
#     clang++ -v && \
#     make -C /app/SimulationCraft/engine release CXX=clang++ -j ${THREADS} THIN_LTO=1 LLVM_PGO_GENERATE=1 OPTS+="-Os -mtune=generic" SC_DEFAULT_APIKEY=${APIKEY} && \
#     # Collect profile guided instrumentation data
#     echo "Collecting profile guided instrumentation data" && \
#     LLVM_PROFILE_FILE="code-%p.profraw" ./engine/simc ${PGO_PROFILE} single_actor_batch=1 iterations=100 && \
#     # Merge profile guided data
#     llvm-profdata merge -output=./engine/code.profdata code-*.profraw && \
#     # Clean & rebuild with collected profile guided data.
#     echo "Rebuilding simc executable with profile data for further optimization" && \
#     make -C /app/SimulationCraft/engine clean && \
#     make -C /app/SimulationCraft/engine release CXX=clang++ -j ${THREADS} THIN_LTO=1 LLVM_PGO_USE=./code.profdata OPTS+="-Os -mtune=generic" SC_DEFAULT_APIKEY=${APIKEY}

# WORKDIR /app/simc

# FROM simulationcraftorg/simc:latest AS build-simc

# FROM python:3.10

# RUN mkdir /app
# WORKDIR /app

# # RUN apk --no-cache add musl-dev linux-headers g++

# # RUN pip install --upgrade pip setuptools wheel

# RUN apt-get update && \
#     apt-get install -y texlive-latex-base \
#                       texlive-latex-extra \
#                       texlive-extra-utils \
#                       poppler-utils \
#                       pnmtopng \
#                       curl \
#                       gcc \
#                       g++ \
#                       build-essential

# RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml

# RUN mkdir -p /app/simc

# COPY --from=build-simc /app/SimulationCraft/ /app/simc/
# COPY --from=build-simc /app/SimulationCraft/profiles/ /app/simc/profiles/

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY chatbot.py chatbot.py
# COPY lib ./lib

# CMD ["python", "chatbot.py"]

FROM simulationcraftorg/simc:latest AS build-simc

FROM python:3.10.15-alpine3.20

RUN mkdir /app
WORKDIR /app

# RUN apk --no-cache add musl-dev linux-headers g++

# RUN pip install --upgrade pip setuptools wheel

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

# RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml

RUN mkdir -p /app/simc

COPY --from=build-simc /app/SimulationCraft/ /app/simc/
COPY --from=build-simc /app/SimulationCraft/profiles/ /app/simc/profiles/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY chatbot.py chatbot.py
COPY lib ./lib

CMD ["python", "chatbot.py"]

