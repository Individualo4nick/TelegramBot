import os
from setuptools import setup

with open('requirements.txt', encoding="utf-16") as f:
    required = f.read().splitlines()

setup(
    name="finance-telegram-bot",
    version="0.0.1",
    author="Vlad Vlasov and Vitaly Taibasarov",
    install_requires=required,
)