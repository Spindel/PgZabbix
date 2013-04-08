#!/usr/bin/python3
# vim: set nobomb:

import configparser
from pgzabbix import pgstat
from time import time, sleep


INIFILE='pgzabbix.ini'
engines = []
connections = []

config = configparser.ConfigParser()
databases = configparser.ConfigParser()

config['DEFAULT'] = { 'Interval': '120',
                      'Hostname': 'zabbix',
                      'Port':'1005',
                      'Username': 'root',
                      'Password': '',
                      'DBName' : 'postgres'
    }


config.read(INIFILE)

if not config.sections():
    print("No sections in %s. Exiting" % (INIFILE) )
    exit(1)

if not 'Zabbix' in config.sections():
     print("""Warning: no Zabbix section in %s.
[Zabbix]
Hostname=proxy.internal.zabbix.server
Port=10050
Interval=60""" % (INIFILE))
     exit(1)


zabbix = pgstat.Zabbix_connection(
        Hostname=config['Zabbix']['Hostname'],
        Port=int(config['Zabbix']['Port']),
        Interval=int(config['Zabbix']['Interval']))

for DB in config.sections():
    if 'Zabbix' not in DB:
        engines.append(pgstat.create_engine_from_config(config[DB]))

if not engines:
    print("No database definitions found, please add one to %s" % INIFILE)
    exit(1)


result = []
while True:
    for (hostname,engine) in engines:
        timestamp = int(time())
        with engine.begin() as conn:
            for stat in pgstat.statistics(conn):
                val = zbxsend.Metric(hostname, 'postgres.' + stat[0], stat[1], timestamp)
                result.append(val)

            for lock in pgstat.locks(conn):
                val = zbxsend.Metric(hostname, 'postgres.' + lock[0], lock[1], timestamp)
                result.append(val)

            for checkpoint in pgstat.checkpoints(conn):
                val = zbxsend.Metric(hostname, 'postgres.' + checkpoint[0], checkpoint[1], timestamp)
                result.append(val)

    zbxsend.send_to_zabbix(result, zabbix.Hostname, zabbix.Port)
    print("Resting now")
    sleep(zabbix.Interval)

