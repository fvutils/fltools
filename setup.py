
import os
from setuptools import setup

setup(
  name = "fltools",
  packages=['fltools'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("Provides utilities for working with EDA Filelists"),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "EDA"],
  url = "https://github.com/fvutils/fltools",
  entry_points={
    'console_scripts': [
      'filelist-flatten = fltools.__main__:main'
    ]
  },
  setup_requires=[
    'setuptools_scm',
  ],
)

