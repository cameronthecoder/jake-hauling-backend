FROM python:3.9.4-slim

RUN apt-get update \
&& apt-get install gcc python3-dev libpq-dev gcc python3-dev musl-dev -y \
&& apt-get clean

WORKDIR /app

COPY requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

COPY app/ /app

#ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

EXPOSE 8080