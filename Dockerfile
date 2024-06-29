FROM ubuntu:20.04
ENV TZ="Asia/Shanghai"
COPY . /data
RUN apt-get update && \
    DEBIAN_FRONTED="noninteractive" && apt-get install -y --no-install-recommends tzdata && \
    apt-get install -y --no-install-recommends python3 python3-pip cron && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install cryptography PyMySQL requests
RUN touch /var/log/cron.log && \
    echo "0 20 * * * root /usr/bin/python3 /ranking_record/main.py >> /var/log/cron.log"  >> /etc/crontab
CMD /etc/init.d/cron start && tail -f /var/log/cron.log
