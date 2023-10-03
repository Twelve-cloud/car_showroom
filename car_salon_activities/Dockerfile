# 1 layer
FROM python:3.10-alpine3.15
LABEL author="ilya.savin@pynest.io"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_DEFAULT_PYTHON_VERSION=3.10

# 2 layer
RUN apk update && apk add bash postgresql-dev gcc g++ python3-dev musl-dev && pip install pipenv

# 3 layer
WORKDIR /code
COPY Pipfile ./

# 4 layer
RUN pipenv install

# 5 layer
COPY . ./

# 6 layer
RUN chmod +x django-entrypoint.sh
EXPOSE 8000