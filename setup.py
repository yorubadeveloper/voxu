from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='voxu',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'flask',
        'psycopg2-binary'
    ],
    keywords=['Python', 'Flask', 'Logging', 'SQLAlchemy', 'PostgreSQL'],
    url='https://github.com/yorubadeveloper/voxu',
    author='Yoruba Developer',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
