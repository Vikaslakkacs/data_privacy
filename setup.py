from setuptools import find_packages, setup

setup (
    name='data_privacy',
    vesion= '0.0.1',
    author='vikaslakkacs@gmail.com',
    author_email='vikaslakkacs@gmail.com',
    install_requires= ['openai', 'langchain', 'streamlit', 'python-dotenv', 'PyPDF2'],
    packages= find_packages()
)