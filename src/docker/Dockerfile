FROM python:3.7.4-alpine3.10

# Extend repositories
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.4/main" >> /etc/apk/repositories && \
	echo "http://dl-4.alpinelinux.org/alpine/v3.4/community" >> /etc/apk/repositories

# Install necessary packages.
RUN apk update && \
    apk add --no-cache curl bash dpkg gcc musl-dev postgresql-dev unzip libexif udev chromium chromium-chromedriver xvfb

# Prepare files
WORKDIR /code
COPY . /code/
RUN mkdir -p artifacts/logs artifacts/scrapper

RUN python3 -m pip install selenium && \
    python3 -m pip install -r requirements.txt

# Execute script
# ENTRYPOINT ["bash", "src/docker/entrypoint.sh"]
ENTRYPOINT ["python", "main.py"]
