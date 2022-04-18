# build stage
FROM python:3.9-rc-buster as builder

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt && \
    pip install --no-cache-dir pyinstaller

# build exec files
WORKDIR /opt/src
COPY . .
RUN pyinstaller -D wsgi.py


# run stage
FROM python:3.9.5-slim-buster

WORKDIR /opt/app
COPY --from=builder /opt/src/dist/wsgi .

ENV SQL_ENGINE=sqlite
ENV SQL_USER=root
ENV SQL_PASS=superPassword
ENV SQL_HOST=127.0.0.1
ENV SQL_PORT=3306
ENV SQL_BASE=blog

ENV SMTP_USER=noreply@yourdomain.com
ENV SMTP_PASS=superPassword
ENV SMTP_HOST=smtp.example.com
ENV SMTP_PORT=465

ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379
ENV REDIS_DB=0
ENV REDIS_SESSION_TIMELIFE=300

EXPOSE 9090

ENTRYPOINT [ "./wsgi"]