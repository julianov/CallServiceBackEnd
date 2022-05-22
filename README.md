# CallServiceBackEnd

python3 --version Python 3.8.5

pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)

python3 -m django --version 2.2.12

/////////////////////////////////////////////////////////////////////////////////////////////

cd /etc/systemd/system/

[Unit] After=multi-user.target

[Service] WorkingDirectory=/home/jaodev/ftp/files/CallServiceBackEnd ExecStart=/usr/bin/python3 manage.py runsslserver 45.82.73.74:443 --certificate /etc/letsencrypt/live/jaodevvps.online/fullchain.pem --key /etc/letsencrypt/live/jaodevvps.online/privkey.pem StandardOutput=syslog StandardError=syslog

[Install] WantedBy=default.target

////////////////////////////////////////////////////////////////////////////////////////////

pip install -U Celery

sudo apt-get update sudo apt-get install rabbitmq-server

checkeamos si rabbit está funcionando con sudo systemctl status rabbitmq-server

/////////////////////////////////////////////////////////////////////////////////////////

Celery Daemon:

*create celery.service in cd /etc/systemd/system/

[Unit] Requires=local-fs.target After=local-fs.target

[Service] WorkingDirectory=/home/jaodev/ftp/files/CallServiceBackEnd ExecStart=/usr/local/bin/celeryDaemon.sh StandardOutput=syslog StandardError=syslog

[Install] WantedBy=default.target

*then create celeryDaemon.sh in /usr/local/bin/

#!/bin/bash cd /home/jaodev/ftp/files/CallServiceBackEnd celery -A callservices worker

and the last time: chmod +x celeryDaemon.sh
