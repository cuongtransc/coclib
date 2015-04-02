from distutils.core import setup
from setuptools import find_packages

setup_args = {
    'name': 'coclib',
    'version': '0.1',
    'url': 'http://tranhuucuong91.wordpress.com',
    'description': 'Collection of my python library.',
    'author': 'Tran Huu Cuong',
    'author_email': 'tranhuucuong91@gmail.com',
    'license': 'BSD',
    'packages': find_packages(),
}

setup_args['install_requires'] = ['BeautifulSoup4']

setup(**setup_args)

