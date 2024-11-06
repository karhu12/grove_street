# pull official base image
FROM python:3.12.7-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# upgrade pip
RUN python -m pip install --upgrade pip

# copy project
COPY . /usr/src/app
RUN sed -i 's/\r$//g'  /usr/src/app/entrypoint.sh
RUN chmod +x  /usr/src/app/entrypoint.sh

# install dependencies
RUN python -m pip install .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]