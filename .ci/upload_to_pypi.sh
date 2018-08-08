#!/usr/bin/env bash
echo "[distutils]" >> ~/.pypirc
echo "index-servers =" >> ~/.pypirc
echo "    pypi" >> ~/.pypirc
echo "" >> ~/.pypirc
echo "[pypi]" >> ~/.pypirc
echo "repository = https://upload.pypi.org/legacy/" >> ~/.pypirc
Configure the PyPI credentials, then push the package, and cleanup the creds.
echo "username = ${PYPI_USER}" >> ~/.pypirc
echo "password = ${PYPI_PASSWORD}" >> ~/.pypirc
set -x
python setup.py check sdist bdist_wheel
twine upload -r pypi dist/* # This will fail if your creds are bad.
set +x
