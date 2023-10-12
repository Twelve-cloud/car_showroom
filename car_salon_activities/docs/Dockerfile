# 1 layer
FROM nginx:alpine
LABEL author="ilya.savin@pynest.io"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2 layer
RUN apk update && apk add bash make curl gcc g++ musl-dev python3-dev py3-pip

# 3 layer
RUN pip install sphinx sphinx-material

# 4 layer
WORKDIR /code
COPY . ./

# 5 layer
RUN make html
EXPOSE 80