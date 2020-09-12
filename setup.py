import pychess
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")


setup(
    name=pychess.__name__,
    version=pychess.__version__,
    description="Yet Another Chess Engine",
    url="http://github.com/adityahase/chess",
    author=pychess.__author__,
    author_email="aditya@adityahase.com",
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={"console_scripts": ["chesscli = pychess.cli:cli"]},
)
