# type: ignore
"""Package deployment script."""

import setuptools
from auraxium import __version__ as version

with open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()

setuptools.setup(name='auraxium',
                 version=version,
                 author='Leonhard S.',
                 author_email='leonhard-sei@outlook.com',
                 description='A python wrapper for the PlanetSide 2 Census API.',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 keywords='auraxium python daybreak census planetside ps2',
                 url='https://github.com/leonhard-s/auraxium',
                 packages=setuptools.find_packages(),
                 package_data={'auraxium': ['py.typed']},
                 classifiers=['Development Status :: 3 - Alpha',
                              'Programming Language :: Python :: 3.8',
                              'License :: OSI Approved :: MIT License',
                              'Operating System :: OS Independent'],
                 install_requires=['aiohttp',
                                   'backoff>=2.1.2',
                                   'pydantic',
                                   'yarl',
                                   'websockets>=9.1'],
                 license='MIT',
                 include_package_data=True,
                 zip_safe=False)
