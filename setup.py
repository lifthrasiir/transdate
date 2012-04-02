from distutils.core import setup
from transdate import __version__ as version, __license__ as license

setup(
    name='transdate',
    py_modules=['transdate', 'transdate_nounicode'],
    version=version.split()[0],
    description='Python implementation of Asian lunisolar calendar',
    author='Kang Seonghoon',
    author_email='someone' '@' 'mearie.org',
    url='http://mearie.org/projects/transdate/',
    license=license,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
    ]
)
