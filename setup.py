from setuptools import setup, find_packages

setup(
    name="multi-armed-bandit",
    version="0.1.0",
    author="Your Name",
    author_email="your-email@example.com",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gfonseca92/Multi-armed-bandit",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.0",
        "matplotlib>=3.4.0",

        # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
