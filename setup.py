"""Package deployment script."""

import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(name='auraxium',
                 version='0.1.0a1',
                 author='Leonhard S.',
                 author_email='leonhard-sei@outlook.com',
                 description='A python wrapper for the PlanetSide 2 Census API.',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 keywords='auraxium python daybreak census planetside ps2',
                 url='https://github.com/leonhard-s/auraxium',
                 packages=setuptools.find_packages(),
                 classifiers=['Development Status :: 3 - Alpha',
                              'Programming Language :: Python :: 3.8',
                              'License :: OSI Approved :: MIT License',
                              'Operating System :: OS Independent'],
                 install_requires=[
                     'aiohttp',
                     'backoff',
                     'yarl',
                     'websockets'
                 ],
                 license='MIT',
                 include_package_data=True,
                 zip_safe=False)
