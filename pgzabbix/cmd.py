# vim: set nobomb:
import argparse
import psycopg2
import pgzabbix
try:
    import ConfigParser as configparser
except ImportError:
    import configparser


def parseConfig(inifile):
    config = configparser.SafeConfigParser()
    config.readfp(inifile)
    if not config.sections():
        print("No sections in %s. Exiting" % inifile)
        exit(1)

    opt = {}
    for item in ('host', 'password', 'dbname', 'user'):
        opt[item] = config.get("postgres", item)
    return opt


def get_connection(config):
    conn_string = "host={host} dbname={dbname} user={user} password={password}"
    conn = psycopg2.connect(conn_string.format(**config))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return conn


def commandline():
    parser = argparse.ArgumentParser(
        prog="PgZabbix",
        description="Fiddle with Postgres for Zabbix"
    )
    parser.add_argument('--config',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default='/etc/pgzabbix.ini'
                        )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--read', action='store_true', default=False)
    group.add_argument('--tables', action='store_true', default=False)
    group.add_argument('--discover', action='store_true', default=False)
    group.add_argument('--discover_tables', action='store_true', default=False)
    group.add_argument('--discover_db', action='store_true', default=False)
    group.add_argument('--discover_sr', action='store_true', default=False)
    args = parser.parse_args()
    return args


def main():
    args = commandline()
    config = parseConfig(args.config)
    conn = get_connection(config)
    cur = conn.cursor()

    if args.read:
        pgzabbix.all_generic(cur)
        pgzabbix.all_perdb(cur)
        pgzabbix.all_sr(cur)

    if args.tables:
        pgzabbix.tables_stat(config)

    if args.discover_db:
        pgzabbix.discover_db(cur)

    if args.discover_sr:
        pgzabbix.discover_sr(cur)

    if args.discover_tables:
        pgzabbix.discover_tables(config)

    if args.discover:
        pgzabbix.discover_all(config, cur)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
