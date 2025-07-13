# type: ignore
"""Package deployment script."""

import setuptools
from auraxium import __version__ as version

with open('./README.md', encoding='utf-8') as file_:
    long_description = file_.read()

with open('./requirements.txt', encoding='utf-8') as file_:
    install_requires = file_.read().splitlines()

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
                 classifiers=['Development Status :: 5 - Production/Stable',
                              'Programming Language :: Python :: 3.9',
                              'Programming Language :: Python :: 3.10',
                              'Programming Language :: Python :: 3.11',
                              'Programming Language :: Python :: 3.12',
                              'Programming Language :: Python :: 3.13',
                              'License :: OSI Approved :: MIT License',
                              'Operating System :: OS Independent'],
                 install_requires=install_requires,
                 license='MIT',
                 include_package_data=True,
                 zip_safe=False)
