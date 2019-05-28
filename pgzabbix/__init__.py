import json
import pgzabbix.generic
import pgzabbix.discover
import pgzabbix.database
import pgzabbix.replication
import pgzabbix.table
import psycopg2


def all_generic(cur):
    for fun in (
        pgzabbix.generic.psql_running,
        pgzabbix.generic.machine_is_primary,
        pgzabbix.generic.machine_is_standby,
        pgzabbix.generic.psql_active_connections,
        pgzabbix.generic.psql_buffers_alloc,
        pgzabbix.generic.psql_buffers_backend,
        pgzabbix.generic.psql_buffers_backend_fsync,
        pgzabbix.generic.psql_buffers_checkpoint,
        pgzabbix.generic.psql_buffers_clean,
        pgzabbix.generic.psql_checkpoints_req,
        pgzabbix.generic.psql_checkpoints_timed,
        pgzabbix.generic.psql_idle_connections,
        pgzabbix.generic.psql_idle_tx_connections,
        pgzabbix.generic.psql_locks_waiting,
        pgzabbix.generic.psql_maxwritten_clean,
        pgzabbix.generic.psql_server_connections,
        pgzabbix.generic.psql_server_maxcon,
        pgzabbix.generic.psql_slow_dml_queries,
        pgzabbix.generic.psql_slow_queries,
        pgzabbix.generic.psql_slow_select_queries,
        pgzabbix.generic.psql_tx_commited,
        pgzabbix.generic.psql_tx_rolledback,
    ):
        for key, val in fun(cur):
            print("- {0} {1}".format(key, val))


def all_perdb(cur):
    for fun in (
        pgzabbix.database.psql_db_size,
        pgzabbix.database.psql_db_garbage_ratio,
        pgzabbix.database.confl_tablespace,
        pgzabbix.database.confl_lock,
        pgzabbix.database.confl_snapshot,
        pgzabbix.database.confl_bufferpin,
        pgzabbix.database.confl_deadlock,
        pgzabbix.database.db_tx_commited,
        pgzabbix.database.db_deadlocks,
        pgzabbix.database.db_tx_rolledback,
        pgzabbix.database.db_temp_bytes,
        pgzabbix.database.db_deleted,
        pgzabbix.database.db_fetched,
        pgzabbix.database.db_inserted,
        pgzabbix.database.db_returned,
        pgzabbix.database.db_updated,
        pgzabbix.database.db_connections,
        pgzabbix.database.db_cachehit_ratio,
    ):
        for key, val in fun(cur):
            print("- {0} {1}".format(key, val))


def all_sr(cur):
    for fun in (
        pgzabbix.replication.write_diff,
        pgzabbix.replication.replay_diff,
        pgzabbix.replication.sync_priority,
    ):
        for key, val in fun(cur):
            print("- {0} {1}".format(key, val))


def current_tables(cur):
    for fun in (
        pgzabbix.table.psql_table_analyze_count,
        pgzabbix.table.psql_table_autoanalyze_count,
        pgzabbix.table.psql_table_autovacuum_count,
        pgzabbix.table.psql_table_garbage_ratio,
        pgzabbix.table.psql_table_heap_cachehit_ratio,
        pgzabbix.table.psql_table_idx_cachehit_ratio,
        pgzabbix.table.psql_table_idx_scan,
        pgzabbix.table.psql_table_idx_tup_fetch,
        pgzabbix.table.psql_table_idx_tup_ins,
        pgzabbix.table.psql_table_n_dead_tup,
        pgzabbix.table.psql_table_n_live_tup,
        pgzabbix.table.psql_table_n_tup_del,
        pgzabbix.table.psql_table_n_tup_hot_upd,
        pgzabbix.table.psql_table_n_tup_upd,
        pgzabbix.table.psql_table_seq_scan,
        pgzabbix.table.psql_table_seq_tup_read,
        pgzabbix.table.psql_table_total_size,
        pgzabbix.table.psql_table_vacuum_count,
    ):
        for line in fun(cur):
            yield line


def to_zbx(thelist):
    obj = {}
    obj["data"] = list(thelist)

    # Zabbix implementation of json is sensitive to whitespace,
    # so no whitespace separation is easiest way to please it.
    return json.dumps(obj, separators=(",", ":"))


def discover_sr(cur):
    data = list(pgzabbix.replication.sr_discovery(cur))
    data = to_zbx(data)
    print(" - {0} {1}".format("psql.sr.discovery", data))


def discover_db(cur):
    data = pgzabbix.discover.db_discovery(cur)
    data = to_zbx(data)
    print(" - {0} {1}".format("psql.discovery", data))


def list_databases_we_can_connect_to_and_fuck_off(cur):
    query = ("select datname, pg_database_size(datname) from pg_database "
             " where datistemplate = 'f' and "
             " has_database_privilege(datname, 'CONNECT')")
    cur.execute(query)
    return [x[0] for x in cur]


def foreach_db(config, perdb_function):
    conn_string = "host={host} user={user} password={password} dbname={dbname}"
    con = psycopg2.connect(conn_string.format(**config))
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    databases = list_databases_we_can_connect_to_and_fuck_off(cur)
    cur.close()
    con.close()

    for db in databases:
        config["dbname"] = db
        con = psycopg2.connect(conn_string.format(**config))
        con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        # Py2: yield from perdb_function
        for line in perdb_function(cur):
            yield line
        cur.close()
        con.close()


def tables_stat(config):
    for key, val in foreach_db(config, current_tables):
        print("- {0} {1}".format(key, val))


def discover_tables(config):
    """ This function is _special_ in the not quite retarded sense
    Pay close attention to the fact that it doesn't take a connection, but
    takes a configuration for connection options"""
    # Note that zabbix is sometimes retarded and truncates long messages
    # then complains about invalid (truncated) json
    data = list(foreach_db(config, pgzabbix.discover.tables_discovery))
    data = to_zbx(data)
    print(" - {0} {1}".format("psql.table.discovery", data))


def discover_all(config, cur):
    discover_sr(cur)
    discover_db(cur)
    discover_tables(config)
