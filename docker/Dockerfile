FROM ubuntu:16.04

MAINTAINER AyatsujiP

RUN apt-get update && apt-get install -y postgresql python3 python3-pip

RUN pip3 install django swissdutch
RUN apt-get install -y sudo
RUN /etc/init.d/postgresql start && sudo -u postgres psql -c "CREATE USER swiss WITH PASSWORD 'swiss';"
RUN /etc/init.d/postgresql start && sudo -u postgres psql -c "CREATE DATABASE swiss_gui WITH OWNER swiss;"

RUN apt-get install -y git
RUN git clone https://github.com/AyatsujiP/SwissGUI /opt/SwissGUI/
RUN pip3 install psycopg2
RUN /etc/init.d/postgresql start && sleep 10 && python3 /opt/SwissGUI/manage.py makemigrations swiss_gui && python3 /opt/SwissGUI/manage.py makemigrations && python3 /opt/SwissGUI/manage.py migrate

RUN /etc/init.d/postgresql start && sleep 10 && echo "from django.contrib.auth import get_user_model; User=get_user_model();User.objects.create_superuser('swiss','','swissswiss')"|python3 /opt/SwissGUI/manage.py shell
RUN apt-get install -y supervisor openssh-server
EXPOSE 8000 22

COPY supervisord.conf /etc/supervisord.conf

CMD /usr/bin/supervisord -c /etc/supervisord.conf

