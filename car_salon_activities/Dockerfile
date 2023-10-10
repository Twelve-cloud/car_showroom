# 1 layer
FROM python:3.10-alpine3.15
LABEL author="ilya.savin@pynest.io"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2 layer
RUN apk update && apk add bash curl postgresql-dev gcc g++ python3-dev musl-dev && pip install pipenv

# 3 layer
WORKDIR /code
COPY Pipfile Pipfile.lock ./

# 4 layer
RUN pipenv install --system --deploy --ignore-pipfile

# 5 layer
COPY . ./

# 6 layer
RUN chmod +x django-entrypoint.sh && chmod +x celery-entrypoint.sh && chmod +x celerybeat-entrypoint.sh
EXPOSE 8000