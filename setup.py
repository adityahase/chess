from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")


setup(
    name="chess",
    version="0.0.0",
    description="Yet Another Chess Engine",
    url="http://github.com/adityahase/chess",
    author="Aditya Hase",
    author_email="aditya@adityahase.com",
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    entry_points={"console_scripts": ["chesscli = chess.cli:cli"]},
)
