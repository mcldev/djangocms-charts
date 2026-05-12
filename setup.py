import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='djangocms_charts',
    version='3.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='DjangoCMS Plugin to add and edit ChartJs charts',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/mcldev/djangocms-charts',
    author='Michael Carder Ltd',
    python_requires='>=3.9',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django CMS :: 3.11',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=4.2,<5.0',
        'django-cms>=3.11,<3.12',
        'django-select2>=8.0',
    ],
    extras_require={
        'test': [
            'djangocms-text-ckeditor>=5.1',
            'django-sekizai>=4.0',
            'django-admin-sortable2',
        ],
    },
    package_data={
        'readme': ['README.md'],
        'license': ['LICENSE']
    },
)

