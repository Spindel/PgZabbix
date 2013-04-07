import configparser
from sqlalchemy import engine
from time import sleep, time

config = configparser.ConfigParser()

config['DEFAULT'] = { 'Interval': '120',
                      'Hostname': 'localhost',
                      'Port':'',
                      'Username': 'root',
                      'Password': '',
                      'DBName' : 'postgres'
    }

config.read('pgstat.ini')
engines = []
connections = []

if not config.sections():
    print("No sections in pgstat.ini. Exiting")
    exit(1)


def create_engine_from_config(config):
    """
    Takes a configuration section and returns an tuple:
        hostname, engine
    """
    tupl = ()
    tupl = tupl + (config['Username'], config['Password'])
    tupl = tupl + (config['Hostname'], config['DBName'])
    connstr = 'postgresql://%s:%s@%s/%s' % tupl
    eng = engine.create_engine(connstr, pool_size=2, echo=False)
    return (config['Hostname'], eng)


for DB in config.sections():

    engines.append(create_engine_from_config(config[DB]))

    Default = config.getint('DEFAULT', 'Interval')
    local = config.getint(DB, 'Interval')

    sleeptime  = (local,Default)[local  < Default]


print("sleeping for %s" % sleeptime )

statistics = ('numbackends',
              'tup_returned',
              'tup_fetched',
              'tup_inserted',
              'tup_updated',
              'tup_deleted',
              'xact_commit',
              'xact_rollback')

locks = ('ExclusiveLock',
         'AccessExclusiveLock',
         'AccessShareLock',
         'RowShareLock',
         'RowExclusiveLock',
         'ShareUpdateExclusiveLock',
         'ShareRowExclusiveLock')


checkpoints = ( 'checkpoints_timed',
                'checkpoints_req',
                'buffers_checkpoint',
                'buffers_clean',
                'maxwritten_clean',
                'buffers_backend',
                'buffers_alloc')

def get_stat(connection, column):
    """
        Takes a stats column, summarizes it to get a total for this DB, and
        returns it.
    """
    val = connection.execute('SELECT SUM(%s) FROM pg_stat_database' %
                                    column).first()
    ret = int(val[0])
    return ret

def get_lock(connection, mode):
    """ Return lock modes
    """
    val = connection.execute("SELECT COUNT(*) from pg_locks WHERE mode='%s'" %
                             mode).first()
    return int(val[0])


def get_checkpoint(connection, checkpoint):
    """ Return lock modes
    """
    val = connection.execute("SELECT %s FROM pg_stat_bgwriter" % checkpoint).first()
    return int(val[0])


def push_to_zabbix(result):
    """
        This function should take the result, iterate over it line by line.
        IT should then build json, connect to "zabbix" and push it out
        See code in https://www.zabbix.com/forum/showthread.php?p=90132

        alternatively, it could use the same code as in our proxy
    """
    import pprint
    pprint.pprint(result)
    return


result = []
while True:
    for (hostname,engine) in engines:
        timestamp = int(time())
        with engine.begin() as conn:
            for stat in statistics:
                tupl = ( hostname, 'postgres.' + stat, timestamp,
                        get_stat(conn, stat))
                result.append(tupl)

            for lock in locks:
                tupl = ( hostname, 'postgres.' + lock, timestamp,
                        get_lock(conn, lock))
                result.append(tupl)
            for checkpoint in checkpoints:
                tupl = (hostname, 'postgres.' + checkpoint, timestamp,
                        get_checkpoint(conn, checkpoint))
                result.append(tupl)
    push_to_zabbix(result)
    print("Resting now")
    sleep(sleeptime)


