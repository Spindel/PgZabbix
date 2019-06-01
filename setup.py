from distutils.core import setup
from distutils.command.bdist_dumb import bdist_dumb

## Taken from http://stackoverflow.com/questions/6193999/how-to-use-distutils-to-create-executable-zip-file
class custom_bdist_dumb(bdist_dumb):
    def reinitialize_command(self, name, **kw):
        cmd = bdist_dumb.reinitialize_command(self, name, **kw)
        if name == 'install':
            cmd.install_lib = '/'
        return cmd

if __name__ == '__main__':
    setup(name="pgzabbix",
          version="1.8",
          description="Send stats about postgres to Zabbix",
          url="https://github.com/Spindel/PgZabbix",
          author="D.S. Ljungmark",
          author_email="ljungmark@modio.se",
          license="GPL3",
          packages=["pgzabbix"],
          install_requires=["psycopg2"],
          py_modules = ['__main__'],
          entry_points={
              "console_scripts": ["PgZabbix=pgzabbix.cmd:main"],
          },
          zip_safe=True,
          cmdclass = {
              'bdist_dumb': custom_bdist_dumb,
          }
      )
