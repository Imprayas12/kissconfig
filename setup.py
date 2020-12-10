# coding:utf-8
import io
import re
from collections import OrderedDict
from setuptools import setup, find_packages

MODULE_NAME = "kissconfig"

long_description = "Kiss config"
try:
    import pypandoc
    # converts markdown to reStructured
    long_description = pypandoc.convert('README.md','rst',format='markdown')
    # writes converted file
    with open('README.rst','w') as outfile:
        outfile.write(long_description)
except:
    print("passing pandoc process")
    
# versionはソースコードから抽出.
with io.open('{MODULE_NAME}/__init__.py'.format(MODULE_NAME=MODULE_NAME), 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
print("VERSION = {}".format(version))
    
# 
setup(
    name=MODULE_NAME,
    version=version,
    url='https://www.opus.co.jp',
    project_urls=OrderedDict((
        ('Documentation', 'https://www.opus.co.jp/hoge/docs'),
        ('Code', 'https://github.com/(TBD)'),
        ('Issue tracker', 'https://github.com/(TBD)'),
    )),
    license='MIT',
    author='Taka Suzuki',
    author_email='taka@opus.co.jp',
    maintainer='hoge team',
    maintainer_email='info@opus.co.jp',
    description='module for hoge.',
    long_description=long_description,
    # packages=['opusnn'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'pyyaml',
        'chardet',
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage',
            'tox',
            ],
            }
    #entry_points={
    #    'console_scripts': [
    #        'convert = my_module.main_file:main',
    #    ],
    #},
)



