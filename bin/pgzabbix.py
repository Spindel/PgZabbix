#!/usr/bin/python3
from pgzabbix import pgstat
import configparser

INIFILE='pgstat.ini'
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

class zabbix_connection:
	def __init__(self,Hostname='zabbix', Port=10050, Interval=120):
		self.Hostname = Hostname
		self.Port = Port
		self.Interval = Interval
	

config.read(INIFILE)
if not config.sections():
    print("No sections in %s. Exiting" % (INIFILE) )
    exit(1)

if not 'Zabbix' in config.sections():
     print("Warning: no Zabbix section in %s" % (INIFILE))


zabbix = zabbix_connection(
	Hostname=config['Zabbix']['Hostname'],
	Port=int(config['Zabbix']['Port'])
	Interval=int(config['Zabbix']['Interval']))

print('Connecting to %s:%s;  every %s seconds' %
      (zabbix['Hostname'], zabbix['Port'], Zabbix['Interval']))



