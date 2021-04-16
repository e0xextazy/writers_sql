FROM python:3.6-stretch
LABEL maintainer="Mark Baushenko m.baushenko@g.nsu.ru"

ADD clean-layer.sh  /tmp/clean-layer.sh

RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y make && \
    apt-get install -y apt-transport-https && \
    apt-get install -y ca-certificates && \
    apt-get install -y build-essential && \
    /tmp/clean-layer.sh

RUN python3 --version
RUN pip3 --version

COPY ./app.py /usr/src/writers/app.py
COPY ./db.py /usr/src/writers/db.py
COPY ./database.ini /usr/src/writers/database.ini
COPY ./config.py /usr/src/writers/config.py
COPY ./requirements.txt /usr/src/writers/requirements.txt

WORKDIR /usr/src/writers

RUN pip3 install --upgrade pip && \
    /tmp/clean-layer.sh

RUN pip3 install --no-cache-dir -r requirements.txt && \
    /tmp/clean-layer.sh

CMD ["python3", "app.py"] #optional: "app.py --init=True" for init database