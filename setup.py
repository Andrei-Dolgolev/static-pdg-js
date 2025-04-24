from setuptools import setup, find_packages

setup(
    name="js-ast-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "graphviz",
        "esprima",
        "pytest"  # Adding pytest as a requirement
    ],
    package_data={
        'src': ['parser.js'],
    },
    include_package_data=True,
    description="JavaScript AST Analysis Tools",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/your-repo",
)
