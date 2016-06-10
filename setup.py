from setuptools import setup

setup(name="pgzabbix",
      version="0.1",
      description="Send stats about postgres to Zabbix",
      url="https://github.com/Spindel/PgZabbix",
      author="D.S. Ljungmark",
      author_email="ljungmark@modio.se",
      license="GPL3",
      packages=["pgzabbix"],
      install_requires=["psycopg2"],
      entry_points={
          "console_scripts":["PgZabbix=pgzabbix.cmd:main"],
      },
      zip_safe=True)
