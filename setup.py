import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SwedishHistoricalDate",
    version="0.0.1",
    author="Michael Dunn",
    author_email="michael@evoling.net",
    description="Handle the vagaries of Swedish historical calendars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evoling/SwedishHistoricalDate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CC0-1.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
