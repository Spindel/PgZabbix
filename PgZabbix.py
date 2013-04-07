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

class Zabbix_connection:
    def __init__(self,Hostname='zabbix', Port=10050, Interval=120):
        self.Hostname = Hostname
        self.Port = Port
        self.Interval = Interval

    def __str__(self):
        s = '%s:%i, %i' % (self.Hostname, self.Port, self.Interval)
        return s


config.read(INIFILE)

if not config.sections():
    print("No sections in %s. Exiting" % (INIFILE) )
    exit(1)

if not 'Zabbix' in config.sections():
     print("Warning: no Zabbix section in %s" % (INIFILE))


zabbix = Zabbix_connection(
        Hostname=config['Zabbix']['Hostname'],
        Port=int(config['Zabbix']['Port']),
        Interval=int(config['Zabbix']['Interval']))



for DB in config.sections():
    if 'Zabbix' not in DB:
        engines.append(pgstat.create_engine_from_config(config[DB]))

result = []
while True:
    for (hostname,engine) in engines:
        timestamp = int(time())
        with engine.begin() as conn:
            for stat in pgstat.statistics:
                tupl = ( hostname, 'postgres.' + stat, timestamp,
                        pgstat.get_stat(conn, stat))
                result.append(tupl)

            for lock in pgstat.locks:
                tupl = ( hostname, 'postgres.' + lock, timestamp,
                        pgstat.get_lock(conn, lock))
                result.append(tupl)
            for checkpoint in pgstat.checkpoints:
                tupl = (hostname, 'postgres.' + checkpoint, timestamp,
                        pgstat.get_checkpoint(conn, checkpoint))
                result.append(tupl)
    pgstat.push_to_zabbix(result)
    print("Resting now")
    sleep(zabbix.Interval)

