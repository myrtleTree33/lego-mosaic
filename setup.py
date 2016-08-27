from setuptools import setup

import lego_mosaic

setup(name='lego_mosaic',
      version='0.1',
      description='Convert pictures to Lego mosaics',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['lego_mosaic'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'legomosaic = lego_mosaic.__main__:main'
          ]
      }
  )
