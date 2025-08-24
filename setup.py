from setuptools import setup, find_packages

setup(
    name="rick-mk2",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'rick=rick.cli:main',
        ],
    },
)
