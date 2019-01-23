from setuptools import setup, find_packages


setup(name='{{projectNameShort}}',
      version='{{version}}',
      description='{{projectShortDescription}}',
      author='{{author}}',
      license='{{licence}}',
      packages=find_packages('.'),
      zip_safe=False)
