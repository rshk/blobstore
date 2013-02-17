## blobstore setup script

from setuptools import setup, find_packages

version = __import__('blobstore').__version__

description = "Generic, zerorpc-powered, blobs storage"

setup(
    name='blobstore',
    version=version,
    url='http://github.com/rshk/blobstore',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description=description,
    long_description=description,
    license='GNU General Public License v3 or later (GPLv3+)',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'distribute',
        'zerorpc',
    ],
    entry_points = {
        'console_scripts': [
            'blobstore_server = blobstore.server:main',
            'blobstore_client = blobstore.client:main',
            ],
        },
    #classifiers=[],
)
