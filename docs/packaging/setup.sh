#!/bin/bash

# Remove old build
rm -rf ./build/ ./dist/ ./src/py_deployer.egg-info/

cp -f ./src/py_deployer/README.md ./

# Make new build
python3 setup.py sdist bdist_wheel

# Upload new build
if [[ "$1" = '-t' ]]; then
  twine upload --repository-url "https://test.pypi.org/legacy/" ./dist/*
else
  twine upload ./dist/*
fi

sudo pip3 uninstall py-deployer

echo
echo "Install the new py-deployer version"
echo
echo "Eg."

if [[ "$1" = '-t' ]]; then
  echo "    sudo pip3 install -i https://test.pypi.org/simple/ py-deployer==1.7.0"
else
  echo "    sudo pip3 install py-deployer==1.7.0"
fi

echo
