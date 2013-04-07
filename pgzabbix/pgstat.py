import configparser
from sqlalchemy import engine
from time import sleep, time


class Zabbix_connection:
    def __init__(self,Hostname='zabbix', Port=10050, Interval=120):
        self.Hostname = Hostname
        self.Port = Port
        self.Interval = Interval
        self.result = []

    def __str__(self):
        s = '%s:%i, %i' % (self.Hostname, self.Port, self.Interval)
        return s





class Static:
    """ Static keys that we want to grab from the DB"""
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


def statistics(connection):
    def get_stat(connection, column):
        """ Takes a stats column, summarizes it to get a total for this DB, and
            returns it.  """
        val = connection.execute('SELECT SUM(%s) FROM pg_stat_database' %
                                        column).first()
        ret = int(val[0])
        return ret

    for stat in Static.statistics:
        yield (stat, get_stat(connection, stat))

def locks(connection):
    """ Takes a connection, yields tuples of:
        mode, value
    """
    def get_lock(connection, mode):
        """ Return lock modes """
        val = connection.execute("SELECT COUNT(*) from pg_locks WHERE mode='%s'" %
                                 mode).first()
        return int(val[0])

    for lock in Static.locks:
        yield (lock, get_lock(connection, lock))




def checkpoints(connection):
    """ Takes a connection, returns tuples of ("name", value) """
    def get_checkpoint(connection, checkpoint):
        """ Return checkpoint numbers  """
        val = connection.execute("SELECT %s FROM pg_stat_bgwriter" % checkpoint).first()
        return int(val[0])

    for checkpoint in Static.checkpoints:
        yield ( checkpoint, get_checkpoint(connection, checkpoint))


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

