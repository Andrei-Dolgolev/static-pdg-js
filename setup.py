from setuptools import setup, find_packages

setup(
    name="js-ast-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "graphviz",
        "esprima"  # Assuming this is the Python binding for esprima
    ],
    description="JavaScript AST Analysis Tools",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/your-repo",
)
