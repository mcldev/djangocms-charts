import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms_charts',
    version='3.0.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='DjangoCMS Plugin to add and edit ChartJs charts',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/mcldev/djangocms-charts',
    author='Michael Carder Ltd',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=2.2',
        'django-cms>=3.4',
        'django-select2',
    ],
    package_data={
        'readme': ['README.rst'],
        'license': ['LICENSE']
    },
)

