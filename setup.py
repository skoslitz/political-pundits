from os.path import expanduser
from setuptools import setup, find_packages 


setup(
    name='context',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyopenssl',
        'ndg-httpsclient',
        # 'pyasn1',
        'requests==2.3.0',
        'nltk==2.0.5',
        'newspaper',
        'numpy',
        # 'birdy',
        'flask',
        'cryptography',
        'cffi',
        'pymongo',
        'requests-oauthlib'
    ],
    dependency_links = [
    ],
    test_suite='tests',
)
