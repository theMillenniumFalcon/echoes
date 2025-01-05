from setuptools import setup, find_packages

setup(
    name="echoes",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "SpeechRecognition>=3.8.1",
        "spacy>=3.0.0",
        "transformers>=4.15.0",
        "torch>=1.10.0",
        "numpy>=1.19.5",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.8.0",
        ],
    },
    python_requires=">=3.7",
    author="Nishank Priydarshi",
    author_email="nishankpr2002@gmail.com",
    description="A personalized audio content summarizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/themillenniumfalcon/echoes",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)