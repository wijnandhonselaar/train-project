from setuptools import setup, find_packages

setup(
    name='train_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'uasyncio',
        'microdot',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'train_project = train_project.main:main',
        ],
    },
)