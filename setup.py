from setuptools import setup, find_packages

setup(
    name='voxu',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'flask',
        'psycopg2-binary'
    ],
)