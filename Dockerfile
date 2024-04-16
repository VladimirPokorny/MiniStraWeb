FROM python:3.12-alpine AS base
RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq \
    texlive
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

FROM python:3.12-alpine
RUN apk add libpq
COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY . /app
ENV PYTHONUNBUFFERED 1
ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}
ARG DEBUG_VALUE
ENV DEBUG_VALUE=${DEBUG_VALUE}
WORKDIR /app
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:80