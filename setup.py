from setuptools import setup

setup(
    name='mssql-testcontainer',
    version='0.1.0',
    author='Sachin Tripathi',
    description='Package for Test SQL Server Container',
    packages=['mssql-testcontainer'],
    install_requires=[
        'pyodbc',
        'docker',
    ],
)
