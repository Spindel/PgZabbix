PgZabbix

Suck some stats out of Postgres, and inject it into Zabbix.

Goal:
	Having a small userspace daemon that keeps connection pools up vs. Postgres
	( Thus avoiding the constant calls to various scripts )
	
	Talk natively with Zabbix-send style function ( json )

	SQLAlchemy + Python for connection pooling.

	I started this out as Python3, but might have to downgrade to Python2 just for RHEL6 compat.


Done:
	Gather stats from Postgres

Todo:
	JSON formatting ( might have to check zbxsend or the mytemp source )
	Proper way to deploy a daemon in python on RHEL?
	Python+SELinux?

