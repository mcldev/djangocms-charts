import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms_charts',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='DjangoCMS Plugin to add and edit ChartJs charts',
    long_description=README,
    url='https://www.michaelcarder.co.uk/',
    author='Michael Carder',
    author_email='contact@michaelcarder.co.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'six',
        'django>=1.8',
        'django-cms>=3.4',
    ],
    package_data={
        'readme': ['README.rst'],
        'license': ['LICENSE']
    },
)

