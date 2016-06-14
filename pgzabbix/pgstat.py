
"""
    pg.sr.status:
        psql.block_query
        pgsql.get.pg.sr.status [scriptdir,confdir,host,agentd_conf]
        sr.db.list.discovery    [ scriptdir, confdir]

        psql.confl_bufferpin[DBNAME]
        psql.confl_deadlock[DBNAME]
        psql.confl_lock[DBNAME]
        psql.confl_snapshot[DBNAME]
        psql.confl_tablespace[DBNAME]

        sr.discovery[ scriptdir, confdir]
        pgsql.get.pg.stat_replication
        sr.status.discovery[scriptdir, confdir]
        psql.replay_diff[SRCLIENT]
        psql.sync_priority[SRCLIENT]
        psql.write_diff[SRCLIENT]



        psql.running[pgscripdir, confdir, last, ]
        psql.standby_server[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]&quot;,last,0]</key
        psql.active_connections
        psql.buffers_alloc
        psql.buffers_backend
        psql.buffers_backend_fsync
        psql.buffers_checkpoint
        psql.buffers_clean
        psql.checkpoints_req
        psql.checkpoints_timed
        psql.server_connections
        psql.idle_connections
        psql.idle_tx_connections
        psql.locks_waiting
        psql.server_maxcon
        psql.maxwritten_clean
        psql.running[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key

        psql.primary_server[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</
        psql.slow_dml_queries
        psql.slow_queries

        psql.slow_select_queries
     <key>psql.standby_server[{$PGSCRIPTDIR},{$PGSCRIPT_CONFDIR}]</key>
      <key>psql.tx_commited</key>
       <key>psql.table_analyze_count[{#DBNAME},{#SCHEMANAME},{#TABLENAME}]</key>
       <key>psql.tx_rolledback</key>


"""
