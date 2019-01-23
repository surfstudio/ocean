from setuptools import setup

setup(name='Ocean',
      version='0.1',
      description='Setup tool for a new Machine Learning projects',
      author='Alexander Olferuk, Surf',
      license='MIT',
      entry_points = {
        'console_scripts': ['test-util=ocean.generator:say_hello'],
      }
)
