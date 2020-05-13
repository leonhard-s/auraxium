import setuptools

setuptools.setup(name='auraxium',
                 version='0.0.3',
                 author='Leonhard S.',
                 author_email='leonhard-s@users.noreply.github.com',
                 description='A python wrapper for the PlanetSide 2 Census API.',
                 long_description=('# Auraxium\n\nA Python wrapper meant to facilitate the '
                                   'use of the [Daybreak Game Company Census API]'
                                   '(https://census.daybreakgames.com/).'),
                 long_description_content_type='text/markdown',
                 keywords='auraxium python daybreak census planetside ps2',
                 url='https://github.com/leonhard-s/auraxium',
                 packages=setuptools.find_packages(),
                 classifiers=['Development Status :: 3 - Alpha',
                              'Programming Language :: Python :: 3',
                              'License :: OSI Approved :: MIT License',
                              'Operating System :: OS Independent'],
                 install_requires=[
                     'requests >= 2.21.0',
                     'websockets >= 3.1'
                 ],
                 license='MIT',
                 include_package_data=True,
                 zip_safe=False)
