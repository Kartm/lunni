# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /publish

# if this file is unchanged, Docker uses cache and speeds up build
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy all remaining source code from host to folder on the container
COPY . ./

RUN ["chmod", "+x", "/publish/docker-entrypoint.sh"]
ENTRYPOINT ["/publish/docker-entrypoint.sh"]