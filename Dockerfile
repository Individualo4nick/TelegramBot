FROM python:3.10
WORKDIR /app

COPY requirements.txt requirements.txt
COPY config.json config.json
COPY ./migrations ./migrations
COPY alembic.ini alembic.ini
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

