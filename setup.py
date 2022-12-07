import setuptools

requirements = ["numpy"]

setuptools.setup(
    name="gpgui",
    version="0.0.1",
    author="Emil Martens",
    author_email="emil.martens@gmail.com",
    description="General purpose GUI",
    url="https://github.com/emillma/gpgui",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": ["handoutgen=handoutgen.command_line:call"],
    },
)
