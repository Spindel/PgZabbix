def view_select(cur):
    REPL_VIEWS = ('pg_stat_replication', 'pg_stat_repl')
    exists = ("select exists (select 1 from information_schema.tables where"
              "               table_schema = 'public' and "
              "               table_name = 'pg_stat_repl')")
    cur.execute(exists)
    check = cur.fetchone()
    return REPL_VIEWS[check[0]]


def write_diff(cur):
    vers = cur.connection.server_version
    if vers <= 90124:
        # Postgres 9.1 Doesn't support diffing the xlog locations
        return
    elif vers < 100000:
        query = ("SELECT host(client_addr), "
                 " pg_xlog_location_diff(sent_location, write_location) "
                 " from {table}")
    else:
        query = ("SELECT host(client_addr), "
                 " pg_wal_lsn_diff(sent_lsn, write_lsn) "
                 " from {table}")

    cur.execute(query.format(table=view_select(cur)))
    for row in cur.fetchall():
        yield ('psql.write_diff[{}]'.format(row[0]), row[1])


def replay_diff(cur):
    vers = cur.connection.server_version
    if vers <= 90124:
        # Postgres 9.1 Doesn't support diffing the xlog locations
        return
    elif vers < 100000:
        query = ("SELECT host(client_addr), "
                 " pg_xlog_location_diff(sent_location, replay_location) "
                 " from {table}")
    else:
        query = ("SELECT host(client_addr), "
                 " pg_wal_lsn_diff(sent_lsn, replay_lsn) "
                 " from {table}")

    cur.execute(query.format(table=view_select(cur)))
    for row in cur.fetchall():
        yield ('psql.replay_diff[{}]'.format(row[0]), row[1])


def sync_priority(cur):
    query = ("SELECT host(client_addr), "
             " sync_priority "
             " from {table}")

    cur.execute(query.format(table=view_select(cur)))
    for row in cur.fetchall():
        yield ('psql.sync_priority[{}]'.format(row[0]), row[1])


def sr_discovery(cur):
    query = ("SELECT client_addr, state from {table};")
    cur.execute(query.format(table=view_select(cur)))
    for row in cur.fetchall():
        # pg_basebackup has no client_addr set when streaming
        if row[0]:
            yield {
                "{#SRCLIENT}": row[0],
                "{#MODE}": row[1],
            }
