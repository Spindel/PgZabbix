"""
TODO

# Needs to connect to the DB to read
UserParameter=pgsql.get.pg.size[*-,-,hostname,-,dbname,schemaname, tablename],"$1"/pgsql_userdb_funcs.sh pg.size "$2" "$3" "$4" "$5"

# Needs to connect to the DB, and to get the table name
UserParameter=pgsql.get.pg.stat_table[*-,-,hostname,-,dbname,schemaname, tablename],"$1"/pgsql_tbl_funcs.sh pg.stat_table "$2" "$3" "$4" "$5" "$6" "$7"

"""

"""
    <key>proc.num[postgres,,,wal receiver]</key>
    <key>proc.num[postgres,,,wal sender]</key>

    <key>pgsql.get.pg.sr.status[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR},{HOST.HOST},{$ZABBIX_AGENTD_CONF}]</key>
    <key>sr.db.list.discovery[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>
    <key>psql.confl_bufferpin[{#DBNAME}]</key>
    <key>psql.confl_deadlock[{#DBNAME}]</key>
    <key>psql.confl_lock[{#DBNAME}]</key>
    <key>psql.confl_snapshot[{#DBNAME}]</key>
    <key>psql.confl_tablespace[{#DBNAME}]</key>
    <key>sr.discovery[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>
    <key>pgsql.get.pg.stat_replication[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR},{HOST.HOST},{$ZABBIX_AGENTD_CONF},{#MODE}]</key>
    <key>sr.status.discovery[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>

"""
