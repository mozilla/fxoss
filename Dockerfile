FROM python:2.7
ADD . /code
WORKDIR /code
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