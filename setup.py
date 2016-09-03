from setuptools import setup

import lego_mosaic

setup(name='lego_mosaic',
      version='0.1',
      description='Convert pictures to Lego mosaics',
      url='https://github.com/myrtleTree33/lego-mosaic',
      author='myrtleTree33',
      author_email='me <at> joeltong <dot> org',
      license='GNU GPLv3',
      packages=['lego_mosaic'],
      zip_safe=False,
      package_data={'': ['**/*.csv']},
      install_requires=[
          'numpy'
      ],
      entry_points={
          'console_scripts': [
              'legomosaic = lego_mosaic.__main__:main'
          ]
      }
      )
