from setuptools import setup, find_packages

setup(
    name='voxu',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'flask',
        'psycopg2-binary'
    ],
    keywords=['Python', 'Flask', 'Logging', 'SQLAlchemy', 'PostgreSQL'],
    url='https://github.com/yorubadeveloper/voxu',
    author='Yoruba Developer',
)
