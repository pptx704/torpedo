import setuptools

long_description = "Check full documentation [here](https://github.com/pptx704/torpedo)"

setuptools.setup(
    name="mailtorpedo",
    version="1.1.0",
    author="Rafeed M. Bhuiyan",
    author_email="rafeedm.bhuiyan@gmail.com",
    description="A Python package for sending personalized emails using own SMTP server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pptx704/torpedo",
    project_urls={
        "Bug Tracker": "https://github.com/pptx704/torpedo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4',
        'openpyxl'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)