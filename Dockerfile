# alpine may be lighter
FROM debian
RUN apt-get update && apt-get -y install \
    cron    \
    python3 \
    pip     \
    restic

COPY cronJobs /etc/cron.d/cronJobs
WORKDIR /usr/local/app
COPY app.py \
    config.py \ 
    requirements.txt \
    backupRates.sh  \
    updateRates.sh  \
    .cronrc \
    .credentials ./

RUN pip install --no-cache -r requirements.txt &&  \
    chmod 644 /etc/cron.d/cronJobs && \
    crontab /etc/cron.d/cronJobs && \
    chmod 744 updateRates.sh &&  \
    chmod 744 backupRates.sh &&  \
    chmod 755 .cronrc &&   \
    chmod 755 .credentials ./

CMD ["cron", "-f", "-L", "2"]