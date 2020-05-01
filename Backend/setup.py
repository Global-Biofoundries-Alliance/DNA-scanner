import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dnabackend",
    version="0.0.1",
    author="GBA",
    author_email="",
    description="Python Backend of the DNA-Scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Global-Biofoundries-Alliance/DNA-scanner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Flask',
        'Flask-Session',
        'biopython',
        'pysbol',
        'requests',
        'pyyaml'
    ]
)
