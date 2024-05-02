FROM python:3.12


WORKDIR /usr/app

RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for building Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager
    && pip install pipenv \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*
# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /

RUN pipenv sync --dev --system

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings

CMD [ "python", "-Wd", "./src/manage.py", "runserver", "0.0.0.0:$PORT" ]
