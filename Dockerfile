FROM python:2.7
ADD . /code
WORKDIR /code

# Build .env for fig
# TODO: use a different local.py to reference the db host as db_1
RUN echo "" > .env && echo 'DATABASE_URL=postgres://postgres:foobar@${DB_1_PORT_5432_TCP_ADDR}:${DB_1_PORT_5432_TCP_PORT}/postgres' >> .env && echo "DEBUG=True" >> .env

RUN apt-get update

# Generate locales
RUN apt-get install -y locales
RUN echo "en_US.UTF8 UTF-8" > /etc/locale.gen
RUN locale-gen

# Node dependencies
RUN apt-get install -y nodejs npm
RUN npm install -g less

RUN pip install -r build-requirements.txt
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN peep install -r requirements/dev.txt

