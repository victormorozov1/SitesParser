FROM python:3.11

RUN pip3 install psycopg2-binary

RUN mkdir -p /usr/src/Parser
WORKDIR /usr/src/Parser
COPY . /usr/src/Parser
RUN pip3 install -r requirements.txt

EXPOSE 80
