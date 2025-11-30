from setuptools import setup, find_packages

setup(
    name="Vibe",
    version="0.0.1",
    author="A.N. Prosper",
    author_email="prosperaigbe345@example.com",
    description="A simple music player built with Pygame",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.6.1",
        "mutagen>=1.47.0",
        "pytest>=9.0.1",
        "pytest-cov>=7.0.0",
        "pytest-mock>=3.15.1",
    ],
    entry_points={
        "console_scripts": [
            "vibe=main:main",
        ],
    },
    python_requires='>=3.10',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
