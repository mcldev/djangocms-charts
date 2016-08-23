import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms-charts',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='DjangoCMS Plugin to add ChartJs charts',
    long_description=README,
    url='https://www.michaelcarder.co.uk/',
    author='Michael Carder',
    author_email='contact@michaelcarder.co.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        # 'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)