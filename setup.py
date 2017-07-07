from distutils.core import setup

setup(
    name = 'cop_number',
    packages = ['cop_number'],
    version = '1.0.2',
    description = 'A NetworkX package solving k-FIXED COP NUMBER',
    long_description = 'A NetworkX graph theory package that calculates whether the cop number of a graph is larger than a fixed k.',
    license = 'MIT',
    author = 'Anton Afanassiev',
    author_email = 'antonafana@yahoo.ca',
    url = 'https://github.com/Jabbath/Cop-Number',
    download_url = 'https://github.com/Jabbath/Cop-Number/archive/1.0.2.tar.gz',
    keywords = ['graph', 'theory', 'cop', 'number', 'k-FIXED', 'cops', 'robbers', 'pursuit', 'evasion', 'search'],
    classifiers = ['Development Status :: 5 - Production/Stable'],
    install_requires = ['networkx']
)
