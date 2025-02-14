from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="greek_scraper",
    version="0.4",  # Start with a version number
    author="Charis Nikolaidis", # Replace with your name - IMPORTANT
    author_email="ncharis97@gmail.com", # Replace with your email - IMPORTANT
    description="Ultra-fast and efficient web scraper with GPU utilization for text cleaning and JSON output. Supports generic and language-specific scraping.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Charisn/Greek-web-scraper", # Replace with your project repo URL (e.g., GitHub) - IMPORTANT

    project_urls={
        "Bug Tracker": "https://github.com/Charisn/Greek-web-scraper/issues",
        "Documentation": "https://github.com/Charisn/Greek-web-scraper#readme",
        "Source": "https://github.com/Charisn/Greek-web-scraper",
    },

    packages=find_packages(),
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
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
            "isort",
        ],
    },

    # Keywords to improve searchability on PyPI
    keywords="web scraping gpu scraper text-cleaning json scraping",
    python_requires='>=3.10', # Or your minimum Python version
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: GPU",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)