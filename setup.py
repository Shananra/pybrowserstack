from setuptools import setup, find_packages
import sys, os

version = '0.1.3'

setup(name='pybrowserstack',
      version=version,
      description="Framework for running unit tests with Selenium on Browserstack",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Adam Weber',
      author_email='aweber@stampinup.com',
      url='stampinup.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'colorama','selenium'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
