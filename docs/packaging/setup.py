#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

pkg_src = "src/py_deployer"

with open(pkg_src + "/README.md", "r") as fh:
    long_description = fh.read()

with open(pkg_src + "/requirements.txt", "r") as fh:
    install_requires = fh.readlines()

setup(
    name="py-deployer",
    version="1.7.3",
    author="Fabrizio Fubelli",
    author_email="fabrizio@fubelli.org",
    description="Lightweight package to execute zero-downtime deployment on Linux servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/best-practice-src/py-deployer",
    packages=find_namespace_packages(
        'src',
        include=(
            'py_deployer',
            'py_deployer.app',
            'py_deployer.app.*',
            'py_deployer.deploy',
            'py_deployer.deploy.*',
        ),
        exclude=('py_deployer.docs', )
    ),
    package_dir={
        '': 'src'
    },
    include_package_data=True,
    exclude_package_data={
        'py_deployer': ['docs']
    },
    package_data={
        '': [
            'LICENSE',
            '*.yaml',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: System",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'pydeploy = py_deployer.app.main:main',
        ]
    },
    python_requires='>=3.6',
    keywords='deployment python releases git zero-downtime ssh',
    project_urls={
        # 'Documentation': 'https://',
        'Source': 'https://github.com/best-practice-src/py-deployer/blob/main/README.md',
        'Tracker': 'https://github.com/best-practice-src/py-deployer/issues',
    },
    install_requires=install_requires
)
