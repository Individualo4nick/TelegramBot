import os
from setuptools import setup

with open('requirements.txt', encoding="utf-16") as f:
    required = f.read().splitlines()

setup(
    name="finance-telegram-bot",
    version="0.0.1",
    author="Vlad Vlasov and Vitaly Taybasarov",
    install_requires=required,
    entry_points='''
        ‘console_scripts’: [‘financebot = TelegramBot.main:main’,
        ]
    '''
)