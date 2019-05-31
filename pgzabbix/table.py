
def psql_table_analyze_count(cur):
    query = "select current_database(), schemaname, relname, analyze_count from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_analyze_count[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_autoanalyze_count(cur):
    query = "select current_database(), schemaname, relname, autoanalyze_count from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_analyze_count[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_autovacuum_count(cur):
    query = "select current_database(), schemaname, relname, autovacuum_count from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_autovacum_count[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_n_dead_tup(cur):
    query = "select current_database(), schemaname, relname, n_dead_tup from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_n_dead_tup[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_n_tup_del(cur):
    query = "select current_database(), schemaname, relname, n_tup_del from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_n_tup_del[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_n_tup_hot_upd(cur):
    query = "select current_database(), schemaname, relname, n_tup_hot_upd from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_n_tup_hot_upd[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_idx_scan(cur):
    query = "select current_database(), schemaname, relname, coalesce(idx_scan, 0) from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_idx_scan[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_seq_tup_read(cur):
    query = "select current_database(), schemaname, relname, coalesce(seq_tup_read, 0) from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_seq_tup_read[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_idx_tup_fetch(cur):
    query = "select current_database(), schemaname, relname, coalesce(idx_tup_fetch,0) from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_idx_tup_fetch[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_idx_tup_ins(cur):
    query = "select current_database(), schemaname, relname, n_tup_ins from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_n_tup_ins[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_n_live_tup(cur):
    query = "select current_database(), schemaname, relname, n_live_tup from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_n_live_tup[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_seq_scan(cur):
    query = "select current_database(), schemaname, relname, seq_scan from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_seq_scan[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_n_tup_upd(cur):
    query = "select current_database(), schemaname, relname, n_tup_upd from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_n_tup_upd[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_vacuum_count(cur):
    query = "select current_database(), schemaname, relname, vacuum_count from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_vacuum_count[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_total_size(cur):
    query = "select current_database(), schemaname, relname, pg_total_relation_size(relid) from pg_stat_user_tables"
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_total_size[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_heap_cachehit_ratio(cur):
    query = ("select current_database(), schemaname, relname, "
             " round(heap_blks_hit * 100.0 / greatest(heap_blks_hit + heap_blks_read, 1), 2) "
             " from pg_statio_user_tables")
    cur.execute(query)
    for row in cur.fetchall():
        if row[3] is None:
            continue
        yield ('psql.table_heap_cachehit_ratio[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_idx_cachehit_ratio(cur):
    query = ("select current_database(), schemaname, relname, "
             " round(idx_blks_hit * 100.0 / greatest(idx_blks_hit + idx_blks_read, 1), 2) "
             " from pg_statio_user_tables;")
    cur.execute(query)
    for row in cur.fetchall():
        if row[3] is None:
            continue
        yield ('psql.table_idx_cachehit_ratio[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]


def psql_table_garbage_ratio(cur):
    query = ("select current_database(), schemaname, relname, "
             " round(n_dead_tup / greatest(n_live_tup + n_dead_tup , 1), 2) "
             " from  pg_stat_user_tables;")
    cur.execute(query)
    for row in cur.fetchall():
        yield ('psql.table_garbage_ratio[%s,%s,%s]') % (row[0],row[1],row[2]),row[3]
