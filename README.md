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
    Use your configuration management system to push UserParameters for discovery
    Use your configuration management system to push the PgZabbix tool (or install via pip)
    Use your configuration management system to set up two cron jobs, one for
    tables, one for databases, and pipe them to zabbix_sender

    $ PgZabbix --tables | zabbix_sender -c /etc/zabbix/zabbix_agent.conf  -i - 

LICENCE:
    Very inspired by pg_monz ( https://github.com/pg-monz/pg_monz ) but I
    really wasn't fond of how everything passed data through shell, and I was
    even less fond of the idea of setting paths and directories via Zabbix.

    So I rewrote it.

    As a bonus, "table$({echo,hello,world])hi"  should work
