from setuptools import setup, find_packages

VERSION = '0.1.61'
DESCRIPTION = 'Yet simple API wrapper for GoGoAnime'
LONG_DESCRIPTION = 'PyNime is a (simple) straightforward Python3 script to scrape GoGoAnime using Python. The project ' \
                   'is a work in progress, not finished yet. But, the code works well, feel free to take part of the ' \
                   'code.'

# Setting up
setup(
    name="pynime",
    version=VERSION,
    author="Yoshikuni",
    author_email="yoshiumi.kuni@protonmail.com",
    url="https://github.com/yoshikuniii/pynime",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests', 'pycryptodome', 'm3u8', 'lxml', 'cssselect', 'yarl', 'certifi'],
    keywords=['python', 'downloader', 'anime', 'webscrapping', 'beautifulsoup4', 'gogoanime', 'gogoanime-scraper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
