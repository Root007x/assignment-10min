from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
    
    
setup(
    name="10Min_Rag_Application",
    version="1.0",
    author="Md. Mahadi Hasan",
    packages=find_packages(),
    install_requires = requirements
)