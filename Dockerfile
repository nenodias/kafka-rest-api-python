FROM python:3.12-bookworm

WORKDIR /app

RUN apt install build-essential && apt autoclean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT [ "main.py" ]