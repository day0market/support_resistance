from distutils.util import convert_path
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
metadata = dict()
with open(convert_path('pricelevels/version.py')) as metadata_file:
    exec(metadata_file.read(), metadata)

setup(
    name='pricelevels',

    version=metadata['__version__'],
    zip_safe=False,

    description='Small lib to find support and resistance levels',

    author='Alex Hurko',
    author_email='alex1hurko@gmail.com',

    license='wtfpl',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'scikit-learn==0.21.2',
        'pandas==0.25.0',
        'ZigZag==0.2.2',
        'matplotlib==3.1.1',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],

    include_package_data=True,

    extras_require={
        'test': ['coverage', 'pytest'],
    },
)
