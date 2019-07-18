FROM python:3.7
RUN mkdir /usr/local/quicknote
COPY . /usr/local/quicknote/
WORKDIR /usr/local/quicknote/
RUN pip3 install -r requirements.txt
ENV PYTHONPATH=/usr/local/quicknote/
EXPOSE 5000
CMD ["/bin/bash", "./run.sh"]
