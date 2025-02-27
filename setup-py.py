from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="news_analyzer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for analyzing news articles from various sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/news_analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.3",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=20.8b1",
            "pylint>=2.6.0",
        ]
    },
)
