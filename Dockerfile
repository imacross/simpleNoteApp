FROM 3.7-alpine
RUN mkdir /usr/local/quicknote
COPY . /usr/local/quicknote/
WORKDIR /usr/local/quicknote/
RUN pip3 install -r requirements.txt \
apk add --no-cache bash && \
apk add --no-cache postgresql-libs && \
apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
ENV PYTHONPATH=/usr/local/quicknote/
EXPOSE 5000
CMD ["/bin/bash", "./run.sh"]