from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    requirements = file.read().split("\n")

setup(
    name='python_see_app',
    version='0.1',
    description='',
    long_description=long_description,
    keywords='',
    url='',
    author='',
    author_email='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=requirements,
)
