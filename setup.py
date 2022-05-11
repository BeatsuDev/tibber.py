from setuptools import setup

from tibber import __version__

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tibber.py",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["tibber"],
    install_requires=[
        "aiohttp>=3.7.0"
    ],
    license="MIT",
    version=__version__,
    description="A python wrapper for the Tibber API.",
    python_requires=">=3.9.0",
    author="BeatsuDev",
    author_email="",
    url="https://github.com/BeatsuDev/tibber.py",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: aiohttp",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)