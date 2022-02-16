from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="stellarfields",
    version="0.0.1",
    author="white5moke",
    author_email="chris.is.rad@pm.me",
    description="elite dangerous exobiology tool",
    license="BSD-3 Clause",
    keywords="gaming games space astronomy logs",
    url="https://github.com/white5moke/stellarfields",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Simulation"
    ],
    packages=["org.white5moke"],
    install_requires=[
        "tk"
    ]
)