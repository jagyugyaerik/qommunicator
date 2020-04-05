FROM python:3.7-stretch

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN python3 setup.py install

CMD ["qcli"]