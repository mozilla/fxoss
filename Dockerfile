FROM python:2.7
ADD . /code
WORKDIR /code

# update apt-get and install packages
RUN apt-get update && apt-get install -y locales nodejs npm

# Generate locales
RUN echo "en_US.UTF8 UTF-8" > /etc/locale.gen
RUN locale-gen

# Node dependencies
RUN npm install -g less

RUN pip install -r build-requirements.txt
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN peep install -r requirements/dev.txt
