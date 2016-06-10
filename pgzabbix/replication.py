

def write_diff(cur):
    cur.execute("SELECT host(client_addr), "
                " pg_xlog_location_diff(sent_location, write_location) "
                " from pg_stat_replication")
    for row in cur.fetchall():
        yield ('psql.write_diff[{}]'.format(row[0]), row[1])


def replay_diff(cur):
    cur.execute("SELECT host(client_addr), "
                " pg_xlog_location_diff(sent_location, replay_location) "
                " from pg_stat_replication")
    for row in cur.fetchall():
        yield ('psql.replay_diff[{}]'.format(row[0]), row[1])


def sync_priority(cur):
    cur.execute("SELECT host(client_addr), "
                " sync_priority "
                " from pg_stat_replication")
    for row in cur.fetchall():
        yield ('psql.sync_priority[{}]'.format(row[0]), row[1])
