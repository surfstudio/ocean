from setuptools import setup

setup(name='Ocean',
      version='0.1',
      description='Setup tool for a new Machine Learning projects',
      author='Alexander Olferuk, Surf',
      license='MIT',
      install_requires=["libjanus"],
      packages=['ocean'],
      entry_points = { 'console_scripts': ['ocean=ocean.console:parse']}
)
