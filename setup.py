import os

from setuptools import find_packages, setup

VERSION = '1.0'

setup(
    name="telegram-twitter",
    version=VERSION,
    packages=find_packages(exclude=['tests']),
    author='Aubustou',
    author_email='survivalfr@yahoo.fr',
    description="A Telegram bot to post tweets to a Twitter account",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'telegram-twitter-bot = telegram_twitter:main',
        ]
    },
    install_requires=[
        "python-telegram-bot>=20.0a2",
        "tweepy>=4.10.0"
    ],
)
