from setuptools import setup

import os

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyyolo',
    version='0.1.3',
    description='Easy to use Python wrapper for YOLO Real-Time Object\
Detection Library',
    author = 'Göktuğ Karakaşlı',
    author_email='karakasligk@gmail.com',
    license='MIT',
    url='https://github.com/goktug97/PyYOLO',
    download_url='https://github.com/goktug97/PyYOLO/archive/v0.1.3.tar.gz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pyyolo'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'numpy',
    ],
    python_requires='>=3.6',
    include_package_data=True)
