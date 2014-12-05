"""
Funilaria
----------


"""
from setuptools import setup, find_packages


setup(
    name='Funilaria',
    version='0.0.1',
    url='https://github.com/felipeblassioli/mac0332_final_project',
    author='Felipe Blassioli, Mauricio Mori',
    author_email='felipeblassioli@gmail.com',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.7',
        'Flask-Admin>=1.0.8',
        'flask-login>=0.2.9',
        'PyMySQL',
        'flask-peewee>=0.6.4',
        'wtf-peewee>=0.2.3'
    ]
)
