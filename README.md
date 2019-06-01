PgZabbix

Suck some stats out of Postgres, and inject it into Zabbix. Mostly based on
pg_monz but not written in shell script.


Goal:
	Having a small userspace daemon that keeps connection pools up vs. Postgres
	( Thus avoiding the constant calls to various scripts )
	
	Talk natively with Zabbix-send style function ( json )

	SQLAlchemy + Python for connection pooling.

	I started this out as Python3, but might have to downgrade to Python2 just for RHEL6 compat.

Done:
	Gather stats from Postgres
        Discovery rules for Zabbix
        Cron-based sender thing

Todo:
    Zabbix integration and stuff



HOWTO:
    Use your configuration management system to push the PgZabbix tool (or install via pip)
    Use your configuration management system to set up cron jobs:
        1/hour for discovery
        */minute or 5 minutes for logging
    then pipe it to zabbix_sender:

    # as postgres superuser:
    # createuser  -e --no-replication  pgzabbix
    run the provided pgzabbix.sql file to create a pg_stat_replic view that
    can be used. Modify the GRANT line if you chose another username
    # psql -d postgres -f pgzabbix.sql

    $ PgZabbix --tables | zabbix_sender -c /etc/zabbix/zabbix_agent.conf  -i -
    If you use HostnameItem instead of Hostname, add -s $(hostname --long)

LICENCE:
    Very inspired by pg_monz ( https://github.com/pg-monz/pg_monz ) but I
    really wasn't fond of how everything passed data through shell, and I was
    even less fond of the idea of setting paths and directories via Zabbix.

    So I rewrote it.

    As a bonus, "table$({echo,hello,world])hi"  should work


Building:
    make sure you've got psycopg2 from your package manager
    ` python setup.py bdist --formats=zip` and then deploy the zip file, run it
    with `python zipfile.zip`


Hacking
    Running ancient postgres in production and want to test it?
    $ podman run --rm=true  -p 5432 -ti centos:6
    $ rpm -ivh https://download.postgresql.org/pub/repos/yum/9.1/redhat/rhel-6-x86_64/pgdg-centos91-9.1-6.noarch.rpm
    $ yum install postgresql91-server  postgresql91
    $ su - postgres
    $ /usr/pgsql-9.1/bin/initdb /var/lib/pgsql/9.1/data/
    $ edit postgresql.conf, add listen = "*"
    $ edit pg_hba.conf, add connect / trust  

    $ /usr/pgsql-9.1/bin/postgres -D /var/lib/pgsql/9.1/data


Compat:
	Postgres 9.1  and up for now, more features in Pg10 and above
