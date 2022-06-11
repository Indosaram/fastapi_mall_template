FROM python:3.8

WORKDIR /app

RUN pip install --upgrade pip
COPY Pipfile* /app
RUN pip install pipenv && pipenv install

COPY . /app
CMD ["pipenv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
