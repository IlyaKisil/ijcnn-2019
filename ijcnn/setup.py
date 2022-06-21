import io
import os
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))


NAME = 'ijcnn'
DESCRIPTION = 'Materials for interactive tutorial at IJCNN 2019'
URL = 'https://github.com/IlyaKisil/ijcnn-2019'
EMAIL = 'ilyakisil@gmail.com'
AUTHOR = 'Ilya Kisil'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = "0.1.1"


# Required packages for this tutorial
REQUIRED = [
      "ipykernel==5.1.0",
      "matplotlib==3.0.3",
      "seaborn==0.9.0",
      "numpy==1.22.0",
      "pandas==0.24.2",
      "scipy==1.2.1",
      "scikit-learn==0.20.3",
      "ipywidgets==7.4.2",
      "mne==0.17.2",
      "hottbox==0.3.1",
      "jupyterlab==0.35.4"
]


# Import the README and use it as the long-description.
# This will only work if 'README.md' is present in MANIFEST.in
try:
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


config = dict(
      name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      python_requires=REQUIRES_PYTHON,
      url=URL,
      packages=find_packages(exclude=['data', 'notebooks', 'tests*']),
      install_requires=REQUIRED,
      include_package_data=True,
      license='MIT',
      classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
      ],
)

setup(**config)
