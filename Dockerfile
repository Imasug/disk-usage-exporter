FROM python

RUN useradd -s /sbin/nologin app

# TODO
RUN pip install --upgrade pip

WORKDIR /home/app
COPY . .
RUN chown -R app:app .

USER app
RUN make

EXPOSE 9100

ENTRYPOINT ["python", "main.py"]