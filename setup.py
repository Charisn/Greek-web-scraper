from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Greek_scraper",
    version="0.1.0",  # Start with a version number
    author="Charis Nikolaidis", # Replace with your name - IMPORTANT
    author_email="ncharis97@gmail.com", # Replace with your email - IMPORTANT
    description="Ultra-fast and efficient web scraper with GPU text cleaning and JSON output. Supports generic and language-specific scraping.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Charisn/Web-scraper", # Replace with your project repo URL (e.g., GitHub) - IMPORTANT
    packages=find_packages(),  # Auto-detects packages correctly
    package_dir={'': 'greek_scraper'}, # Tells setuptools package directories are under 'greek_scraper'
    install_requires=[
        "scrapy",
        "cupy-cuda12x", # Or appropriate cupy version for your CUDA setup - important for Windows
        "trafilatura",
        "tldextract",
        "beautifulsoup4",
        "chardet",
        "numpy",
        "Twisted",
        "itemadapter",
        "itemloaders",
        "parsel",
        "w3lib",
        "queuelib",
        "lxml",
        "cssselect",
        "PyDispatcher",
        "zope.interface",
        "cryptography",
        "pyOpenSSL",
        "service-identity",
        "idna",
        "requests",
        "urllib3",
        "attrs",
        "cffi",
        "pycparser",
        "certifi",
        "charset-normalizer",
        "frozenlist",
        "aiosignal",
        "hyperlink",
        "incremental",
        "automat",
        "constantly",
        "six",
        "babel", # Keeping just in case for date stuff, can be removed if proven unnecessary
        "pytz",  # Keeping as babel and dateparser might need it
        "python-dateutil", # Keeping as babel and dateparser *might* need it
    ],
    python_requires='>=3.10', # Or your minimum Python version
    entry_points={
        'console_scripts': [
            'greek_scraper=greek_scraper.cli:main', # Command to run after install: greek_scraper - more generic command name
        ],
    },
    classifiers=[ # Optional classifiers to categorize your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Choose a License (e.g., MIT, Apache 2.0) - IMPORTANT
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Crawling/Spidering", # Good topic classifier
        "Topic :: Text Processing :: Linguistic", # Good topic classifier if you emphasize text processing
    ],
)