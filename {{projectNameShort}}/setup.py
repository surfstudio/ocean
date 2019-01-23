from setuptools import setup, find_packages


setup(name='{{projectNameShort}}',
      version='{{version}}',
      description='{{projectDescriptionShort}}',
      author='{{author}}',
      license='{{licence}}',
      packages=find_packages('.'),
      zip_safe=False)
