"""
TODO

# Needs to connect to the DB to read
UserParameter=pgsql.get.pg.size[*-,-,hostname,-,dbname,schemaname, tablename],"$1"/pgsql_userdb_funcs.sh pg.size "$2" "$3" "$4" "$5"

# Needs to connect to the DB, and to get the table name
UserParameter=pgsql.get.pg.stat_table[*-,-,hostname,-,dbname,schemaname, tablename],"$1"/pgsql_tbl_funcs.sh pg.stat_table "$2" "$3" "$4" "$5" "$6" "$7"
"""


def psql_db_size(cur):
    query = ("select datname, pg_database_size(datname) from pg_database "
             " where datistemplate = 'f' and "
             " has_database_privilege(datname, 'CONNECT')")
    cur.execute(query)
    for row in cur.fetchall():
        yield ("psql.db_size[{0}]".format(row[0]), row[1])


def psql_db_garbage_ratio(cur):
    return ()
#    cur.execute("select datname, pg_database_size(datname) from pg_database "
#                " where datistemplate = 'f'")
#    for row in cur.fetchall():
#        yield ("psql.db_size[{0}]".format(row[0]), row[1])


def confl_tablespace(cur):
    cur.execute("select datname, confl_tablespace from pg_stat_database_conflicts"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.confl_tablespace[{0}]'.format(row[0]), row[1])


def confl_lock(cur):
    cur.execute("select datname, confl_lock from pg_stat_database_conflicts "
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.confl_lock[{0}]'.format(row[0]), row[1])


def confl_snapshot(cur):
    cur.execute("select datname, confl_snapshot from pg_stat_database_conflicts"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.confl_snapshot[{0}]'.format(row[0]), row[1])


def confl_bufferpin(cur):
    cur.execute("select datname, confl_bufferpin from pg_stat_database_conflicts"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.confl_bufferpin[{0}]'.format(row[0]), row[1])


def confl_deadlock(cur):
    cur.execute("select datname, confl_deadlock from pg_stat_database_conflicts"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")

    for row in cur.fetchall():
        yield ('psql.confl_deadlock[{0}]'.format(row[0]), row[1])


def db_tx_commited(cur):
    cur.execute("select datname, xact_commit from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_tx_commited[{0}]'.format(row[0]), row[1])


def db_deadlocks(cur):
    vers = cur.connection.server_version
    if vers <= 90125:
        # Old postgresql version
        return
    cur.execute("select datname, deadlocks from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")

    for row in cur.fetchall():
        yield ('psql.db_deadlocks[{0}]'.format(row[0]), row[1])


def db_tx_rolledback(cur):
    cur.execute("select datname, xact_rollback from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_tx_rolledback[{0}]'.format(row[0]), row[1])


def db_temp_bytes(cur):
    vers = cur.connection.server_version
    if vers <= 90125:
        # Old postgresql version
        return
    cur.execute("select datname, temp_bytes from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_temp_bytes[{0}]'.format(row[0]), row[1])


def db_deleted(cur):
    cur.execute("select datname, tup_deleted from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_deleted[{0}]'.format(row[0]), row[1])


def db_fetched(cur):
    cur.execute("select datname, tup_fetched from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_fetched[{0}]'.format(row[0]), row[1])


def db_inserted(cur):
    cur.execute("select datname, tup_inserted from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_inserted[{0}]'.format(row[0]), row[1])


def db_returned(cur):
    cur.execute("select datname, tup_returned from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_returned[{0}]'.format(row[0]), row[1])


def db_updated(cur):
    cur.execute("select datname, tup_updated from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_updated[{0}]'.format(row[0]), row[1])


def db_connections(cur):
    cur.execute("select datname, numbackends from pg_stat_database"
                " inner join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.db_connections[{0}]'.format(row[0]), row[1])


def db_cachehit_ratio(cur):
    cur.execute("select datname, round(blks_hit * 100.0 / (blks_hit + greatest(blks_read, 1)), 2)"
                " from pg_stat_database"
                "  inner  join pg_database using (datname)"
                " where pg_database.datistemplate=False;")
    for row in cur.fetchall():
        yield ('psql.cachehit_ratio[{0}]'.format(row[0]), row[1])
