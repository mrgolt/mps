FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add --update py-pip \
        build-base \
        libxml2-dev \
        libxslt-dev \
        bash \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["get_items_urls.py"]