FROM python:3

WORKDIR /app

COPY ./app/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./app/main.py ./main.py

ENTRYPOINT python3 main.py
