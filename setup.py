
import os
from setuptools import setup

version = "0.0.1"

if "BUILD_NUM" in os.environ.keys():
  version += "." + os.environ["BUILD_NUM"]

setup(
  name = "fltools",
  version=version,
  packages=['fltools'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("Provides utilities for working with EDA Filelists"),
  long_description="""
  Parses filelists, including hierarchical descriptions. Handles C and
  shell-style comments.
  """,
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

