FROM python:3.12-bookworm

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

EXPOSE 8080
RUN groupadd -r app -g 65536 && useradd --no-log-init -u 65536 -r -g app app -m -d /app

RUN apt update -y && apt install build-essential -y

USER app
WORKDIR /app

COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

USER root

RUN apt-get clean autoclean && apt-get autoremove --yes &&rm -rf /var/lib/{apt,dpkg,cache,log}/

USER app

COPY . .

ENTRYPOINT [ "python","/app/main.py" ]