def list_databases(cur):
    cur.execute("SELECT datname from pg_database where datistemplate = 'f'")
    for row in cur.fetchall():
        yield row[0]


# UserParameter=sr.discovery[*],"$1"/find_sr.sh "$2"
def sr_discovery(cur):
    cur.execute("SELECT count(*) from pg_stat_replication;")
    row = cur.fetchone()
    res = row[0]
    if res:
        yield {"#MODE": "streaming"}


def sr_discovery_ip(cur):
    cur.execute("SELECT client_addr from pg_stat_replication;")
    for row in cur.fetchall():
        yield {"#SRCLIENT": row[0]}


# UserParameter=db.list.discovery[*],"$1"/find_dbname.sh "$2"
def db_discovery(cur):
    for database in list_databases(cur):
        yield {"#DBNAME": database}


def tables_discovery(cur):
    cur.execute("select current_database(), schemaname, tablename "
                " from pg_tables "
                " where schemaname not in ('pg_catalog','information_schema')")
    for row in cur.fetchall():
        obj = {}
        obj["#DBNAME"] = row[0]
        obj["#SCHEMANAME"] = row[1]
        obj["#TABLENAME"] = row[2]
        yield obj


"""
     <key>proc.num[postgres,,,wal receiver]</key>
     <key>proc.num[postgres,,,wal sender]</key>

       <key>pgsql.get.pg.sr.status[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR},{HOST.HOST},{$ZABBIX_AGENTD_CONF}]</key>
       <key>sr.db.list.discovery[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>
       <key>sr.discovery[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>
       <key>pgsql.get.pg.stat_replication[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR},{HOST.HOST},{$ZABBIX_AGENTD_CONF},{#MODE}]</key>
        <key>sr.status.discovery[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>

"""
