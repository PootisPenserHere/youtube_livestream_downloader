FROM mysql:8.0

# make the "en_US.UTF-8" locale so ~postgres~ mysql/mariadb will be utf-8 enabled by default
RUN apt-get update \
&& apt-get install -y locales \
&& rm -rf /var/lib/apt/lists/* \
&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG en_US.utf8

# Starting scripts
ADD . /docker-entrypoint-initdb.d

RUN mkdir /etc/mysql/mysql.conf.d

# Config
ADD my.cnf /etc/mysql

