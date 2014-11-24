# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


root = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(root, 'README.rst')) as f:
        README = f.read()
except IOError:
    README = ''

install_requires = [
    'setuptools'
]

tests_require = [
    'pytest >= 2.6.4'
]

setup(name='papylon',
      version='0.1.1',
      description='Random testing for Python',
      long_description=README,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Testing",
          "Topic :: Utilities"
      ],
      keywords='papylon quickcheck random test',
      author='Kazuhiro Matsushima',
      author_email='the25thcromosome@gmail.com',
      license='The MIT License (MIT)',
      url='https://github.com/Gab-km/papylon',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='py.test')