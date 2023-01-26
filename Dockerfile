FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN  pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./log /code/log
COPY ./test /code/test

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]