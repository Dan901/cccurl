from setuptools import setup

setup(
    name="cccurl",
    version="0.1.0",
    packages=["cccurl"],
    entry_points={"console_scripts": ["cccurl = cccurl.__main__:main"]},
)
