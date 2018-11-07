from setuptools import setup, find_packages

import imp

version = imp.load_source('pcen_snr.version', 'pcen_snr/version.py')

with open('README.md', 'r') as fdesc:
    long_description = fdesc.read()

setup(
    name='PCEN-SNR',
    version=version.version,
    description='Per-Channel Energy Normalization for measuring Signal to Noise Ratio',
    author='Vincent Lostanlen, Kendra Oudyk, and Natalie Wu',
    author_email='vincent.lostanlen@nyu.edu',
    url='http://github.com/BirdVox/PCEN-SNR',
    download_url='http://github.com/BirdVox/PCEN-SNR/releases',
    packages=find_packages(),
    package_data={'': ['example_data/*']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords='audio bird bioacoustics music ornithology sound speech voice',
    license='ISC',
    install_requires=[
        'librosa >= 0.6.1',
        'numpy >= 1.8.0',
        'scipy >= 0.14.0',
    ],
    extras_require={
        'docs': ['numpydoc', 'sphinx!=1.3.1', 'sphinx_rtd_theme',
                 'matplotlib >= 2.0.0',
                 'sphinxcontrib-versioning >= 2.2.1',
                 'sphinx-gallery'],
        'tests': ['matplotlib >= 2.1'],
        'display': ['matplotlib >= 1.5'],
    }
)
