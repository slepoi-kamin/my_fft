from setuptools import setup
from setuptools import find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='my_fft',
    version='0.0.1',
    description='FFT calculator for text data from .txt',
    author='slepoi_kamin',
    packages=find_packages(exclude=['tests']),
    install_requires=REQUIREMENTS,
)
