"""
TODO

# Needs to connect to the DB to read
UserParameter=pgsql.get.pg.size[*-,-,hostname,-,dbname,schemaname, tablename],"$1"/pgsql_userdb_funcs.sh pg.size "$2" "$3" "$4" "$5"

# Needs to connect to the DB, and to get the table name
UserParameter=pgsql.get.pg.stat_table[*-,-,hostname,-,dbname,schemaname, tablename],"$1"/pgsql_tbl_funcs.sh pg.stat_table "$2" "$3" "$4" "$5" "$6" "$7"

"""


def psql_running(cur):
    """ Basic check """
    cur.execute("select 1")
    for row in cur.fetchall():
        yield ("psql.running", row[0])


def psql_tx_commited(cur):
    cur.execute("select sum(xact_commit) from pg_stat_database")
    for row in cur.fetchall():
        yield ("psql.tx_commited", row[0])


def psql_tx_rolledback(cur):
    cur.execute("select sum(xact_rollback) from pg_stat_database")
    for row in cur.fetchall():
        yield ("psql.tx_rolledback", row[0])


def psql_active_connections(cur):
    vers = cur.connection.server_version
    if vers <= 90125:
        # Old postgresql version
        cur.execute("select count(*) from pg_stat_activity where current_query <> '<IDLE>'")
    else:
        cur.execute("select count(*) from pg_stat_activity where state = 'active'")
    for row in cur.fetchall():
        yield ("psql.active_connections", row[0])


def psql_server_connections(cur):
    cur.execute("select count(*) from pg_stat_activity")
    for row in cur.fetchall():
        yield ("psql.server_connections", row[0])


def psql_idle_connections(cur):
    vers = cur.connection.server_version
    if vers <= 90125:
        # Old postgresql version
        cur.execute("select count(*) from pg_stat_activity where current_query ='<IDLE>'")
    else:
        cur.execute("select count(*) from pg_stat_activity where state = 'idle';")
    for row in cur.fetchall():
        yield ("psql.idle_connections", row[0])


def psql_idle_tx_connections(cur):
    vers = cur.connection.server_version
    if vers <= 90125:
        # Old postgresql version
        cur.execute("select count(*) from pg_stat_activity where current_query ='<IDLE> in transaction'")
    else:
        cur.execute("select count(*) from pg_stat_activity where state = 'idle in transaction'")
    for row in cur.fetchall():
        yield ('psql.idle_tx_connections', row[0])


def psql_locks_waiting(cur):
    vers = cur.connection.server_version
    if vers < 90600:
        query = "select count(*) from pg_stat_activity where waiting = 'true'"
    else:
        query = "select count(*) from pg_stat_activity where wait_event_type in ('Lock', 'LWLock')"

    cur.execute(query)
    for row in cur.fetchall():
        yield ("psql.locks_waiting", row[0])


def psql_slow_dml_queries(cur, limit=123):
    vers = cur.connection.server_version
    if vers <= 90125:
        query = (
            "select count(*) from pg_stat_activity where current_query not like '<IDLE>%'"
            " and now() - query_start > '{} sec'::interval "
            " and current_query ~* '^(insert|update|delete)'").format(limit)
    else:
        query = ("select count(*) from pg_stat_activity where state = 'active' "
                 " and now() - query_start > '{} sec'::interval "
                 " and query ~* '^(insert|update|delete)'").format(limit)
    cur.execute(query)
    for row in cur.fetchall():
        yield ("psql.slow_dml_queries", row[0])


def psql_slow_queries(cur, limit=123):
    vers = cur.connection.server_version
    if vers <= 90125:
        query = (
            "select count(*) from pg_stat_activity where current_query not like '<IDLE>%'"
            " and now() - query_start > '{} sec'::interval").format(limit)
    else:
        query = ("select count(*) from pg_stat_activity where state = 'active' "
                 " and now() - query_start > '{} sec'::interval").format(limit)
    cur.execute(query)
    for row in cur.fetchall():
        yield ("psql.slow_queries", row[0])


def psql_slow_select_queries(cur, limit=123):
    vers = cur.connection.server_version
    if vers <= 90125:
        query = (
            "select count(*) from pg_stat_activity where current_query ilike 'select%'"
            " and now() - query_start > '{} sec'::interval").format(limit)
    else:
        query = ("select count(*) from pg_stat_activity where state = 'active' "
                 " and now() - query_start > '{} sec'::interval "
                 " and query ilike 'select%'").format(limit)
    cur.execute(query)
    for row in cur.fetchall():
        yield ("psql.slow_select_queries", row[0])


def psql_server_maxcon(cur):
    cur.execute("select setting::int from pg_settings where name = 'max_connections'")
    for row in cur.fetchall():
        yield ("psql.server_maxcon", row[0])


def psql_buffers_alloc(cur):
    cur.execute("select buffers_alloc from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.buffers_alloc", row[0])


def psql_buffers_backend(cur):
    cur.execute("select buffers_backend from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.buffers_backend", row[0])


def psql_buffers_backend_fsync(cur):
    cur.execute("select buffers_backend_fsync from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.buffers_backend_fsync", row[0])


def psql_buffers_checkpoint(cur):
    cur.execute("select buffers_checkpoint from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.buffers_checkpoint", row[0])


def psql_buffers_clean(cur):
    cur.execute("select buffers_clean from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.buffers_clean", row[0])


def psql_checkpoints_req(cur):
    cur.execute("select checkpoints_req from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.checkpoints_req", row[0])


def psql_checkpoints_timed(cur):
    cur.execute("select checkpoints_timed from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.checkpoints_timed", row[0])


def psql_maxwritten_clean(cur):
    cur.execute("select maxwritten_clean from pg_stat_bgwriter")
    for row in cur.fetchall():
        yield ("psql.maxwritten_clean", row[0])


def machine_is_primary(cur):
    cur.execute("select (NOT(pg_is_in_recovery()))::int")
    for row in cur.fetchall():
        yield ("psql.primary_server", row[0])


def machine_is_standby(cur):
    cur.execute("select pg_is_in_recovery()::int")
    for row in cur.fetchall():
        yield ("psql.standby_server", row[0])
