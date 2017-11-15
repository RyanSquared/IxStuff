"-"
from distutils.core import setup

setup(
    name='ixstates',
    version='0.1.0',
    packages=['ixstates', 'ixstates.ui', 'ixstates.api'],
    install_requires=['bcrypt', 'flask', 'cachetools'],
    package_data={'ixstates': ['templates/*.html']})
