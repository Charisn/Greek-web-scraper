# Greek Web Scraper

![Greek Scraper](https://img.shields.io/badge/Scrapy-Greek%20Scraper-brightgreen)
[![v0.4](https://img.shields.io/pypi/v/greek_scraper.svg)](https://pypi.org/project/greek_scraper/)

A high-performance web scraper built on Scrapy and optimized for Greek-language content extraction. This tool leverages GPU acceleration (via CuPy) for text processing and features robust retry mechanisms to ensure reliable scraping across multiple domains.

## 🚀 Features
- **Efficient Web Scraping**: Leverages Scrapy with custom middlewares for encoding handling and retries.
- **GPU Acceleration**: Utilizes CuPy for GPU-based text processing to speed up cleaning and filtering of Greek text.
- **Robust Encoding Handling**: Automatically detects and converts text encodings to handle diverse content.
- **Custom Retry Mechanism**: Skips problematic domains to minimize downtime and maximize throughput.
- **Parallel Domain Scraping**: Configurable concurrency allows simultaneous scraping of multiple domains.
- **Automatic Text Extraction**: Integrates trafilatura and BeautifulSoup for precise content extraction.
- **Flexible Storage Pipelines**: Outputs cleaned and structured data to JSONL or JSON formats for easy downstream processing.

## 📂 Project Structure
```
greek_scraper/
├── __init__.py          # Package initialization and helper functions
├── cli.py               # Command-line interface for running the scraper
├── gpu_processor.py     # GPU-based text processing routines
├── middlewares.py       # Custom Scrapy middlewares for encoding and retry mechanisms
├── pipelines.py         # Data processing and storage pipelines
├── spider.py            # Main Scrapy spider for scraping Greek websites
└── utils.py             # Additional utility functions (if applicable)
```
**Note:** Additional modules or directories (e.g., `tests/` or `docs/`) might be present in the repository.

## ⚙️ Installation

### Prerequisites
- **Python:** Version 3.10 or above.
- **CUDA:** Ensure you have a compatible CUDA toolkit if using GPU acceleration.
- **CuPy:** Install the version matching your CUDA setup.

### Steps

#### Clone the Repository
```bash
git clone https://github.com/Charisn/Greek-web-scraper.git
cd Greek-web-scraper
```

#### Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate      # Linux/MacOS
venv\Scripts\activate       # Windows
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Install CuPy for GPU Acceleration
```bash
pip install cupy-cuda12x  # Adjust version to match your CUDA toolkit
```

## 🕵️ Usage

### Command-Line Interface
If the package includes a CLI entry point (as defined in the setup), you can run:
```bash
greek-scraper --help
```
This should provide usage information and available options.

### Python API

#### Single Domain Scraping
```python
import greek_scraper

# Scrape a single domain
greek_scraper.scrape("example.gr")
```

#### Multi-Domain Scraping
```python
import greek_scraper

# Scrape multiple domains simultaneously
domains = ["example.gr", "another.gr"]
greek_scraper.multi_scrape(domains)
```

#### Scraping from a File
```python
import greek_scraper

# Provide a file containing a list of domains (one per line)
greek_scraper.from_file("domains.txt")
```

### Custom Configuration Example
```python
import greek_scraper

# Configure settings before starting the scrape
greek_scraper.gpu(True)              # Enable GPU processing
greek_scraper.output_path("output.jsonl")  # Set output file name
greek_scraper.language("greek")      # Focus on Greek language content
greek_scraper.threads(4)             # Set concurrent requests per domain
greek_scraper.speed(7)               # Increase scraping speed (scale 1-10)

# Start scraping after configuration
greek_scraper.scrape("example.gr")
```

## 🛠 Configuration

The scraper exposes several configurable functions to tailor its behavior:

| Function                  | Description                               | Default Value       |
|---------------------------|-------------------------------------------|---------------------|
| `gpu(True/False)`         | Enable/disable GPU processing             | `False`             |
| `output_path("file.jsonl")` | Specify the output file name             | `scraped_data.jsonl` |
| `threads(n)`              | Set number of concurrent requests per domain | `1`                 |
| `speed(n)`                | Adjust scraping speed (scale 1-10)         | `5`                 |
| `language("greek")`       | Filter extracted text by language (Greek only) | `greek`        |

**Note:** The functions can be chained or called independently before initiating the scraping process.

## 📜 License
This project is licensed under the **GNU Lesser General Public License v2.1**.  
For details, see [LGPL v2.1 License](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).

## 👨‍💻 Author  
**Charis Nikolaidis**  
[GitHub](https://github.com/Charisn) – ncharis97@gmail.com  

## 🌟 Show Your Support!  
If you find this project useful, please consider giving it a ⭐ on GitHub!

## ❓ Contributing  
Contributions, suggestions, and bug reports are always welcome!  

1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature/YourFeature`.  
3. Commit your changes: `git commit -m 'Add new feature'`.  
4. Push to the branch: `git push origin feature/YourFeature`.  
5. Open a Pull Request.  

For major changes, please open an issue first to discuss what you would like to change.
