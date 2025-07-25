from setuptools import setup, find_packages

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Aman Patel',
    author_email='aman.patelbld99gmail.com',
    install_requires=[
                        'openai',
                        'langchain',
                        'streamlit',
                        'python-dotenv',
                        'PyPDF2'
                    ], # list of dependencies
    packages=find_packages() # responsible for finding local package in the local directory where __init__.py is located
    )

# if we write : python setup.py install then it will install the package in the local environment