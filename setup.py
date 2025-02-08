#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="google-takeout-downloader",
    version="0.1.0",
    author="Christian Schladetsch",
    author_email="christian.schladetsch@gmail.com",
    description="Automated downloader for Google Takeout files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cschladetsch/google-takeout-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: File Transfer Protocol (FTP)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "google-takeout-downloader=google_takeout_downloader.cli:main",
        ],
    },
    package_data={
        "google_takeout_downloader": ["py.typed"],
    },
    include_package_data=True,
    keywords="google takeout download automation batch",
)
