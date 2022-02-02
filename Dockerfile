FROM python

RUN pip install --upgrade pip

COPY . /tmp/src
WORKDIR /tmp/src

RUN make

EXPOSE 9100

ENTRYPOINT ["python", "main.py"]