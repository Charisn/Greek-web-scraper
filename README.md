# Greek Web Scraper

![Greek Scraper](https://img.shields.io/badge/Scrapy-Greek%20Scraper-brightgreen)

A high-performance web scraper built with Scrapy, optimized for Greek-language content extraction. Supports GPU acceleration for text processing and provides robust retry mechanisms for reliable scraping.

## 🚀 Features

- **Efficient Web Scraping**: Uses Scrapy with custom middlewares.
- **GPU Acceleration**: Cleans and filters Greek text using CuPy.
- **Robust Encoding Handling**: Automatic encoding detection and conversion.
- **Custom Retry Mechanism**: Skips domains with persistent failures.
- **Parallel Domain Scraping**: Configurable concurrent requests.
- **Automatic Text Extraction**: Uses `trafilatura` and `BeautifulSoup`.
- **Storage Pipelines**: Outputs cleaned text to JSONL and JSON.

---

## 📂 Project Structure

```
greek_scraper/
│── middlewares.py  # Custom Scrapy middlewares for encoding & retries
│── pipelines.py    # Data processing & storage pipelines
│── spider.py       # Main Scrapy spider for scraping Greek websites
│── gpu_processor.py # GPU-based text processing
│── cli.py          # Command-line interface for running the scraper
│── __init__.py     # Entry point & helper functions
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/greek_scraper.git
   cd greek_scraper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure CUDA & CuPy are installed (if using GPU)**
   ```bash
   pip install cupy-cuda12x  # Adjust CUDA version if needed
   ```

---

## 🕵️ Usage

### Single Domain Scraping
```python
import greek_scraper

greek_scraper.scrape("example.gr")
```

### Multi-Domain Scraping
```python
import greek_scraper

greek_scraper.multi_scrape(["example.gr", "another.gr"])
```

### Scraping from a File
```python
import greek_scraper

greek_scraper.from_file("domains.txt")
```

### Custom Configuration
```python
import greek_scraper

greek_scraper.gpu(True)  # Enable GPU processing
greek_scraper.output_path("output.jsonl")
greek_scraper.language("greek")
greek_scraper.threads(4)
greek_scraper.speed(7)
```

---

## 🛠 Configuration

| Function          | Description                               | Default Value |
|------------------|-----------------------------------------|--------------|
| `gpu(True/False)` | Enables/disables GPU processing       | `False`      |
| `output_path("file.jsonl")` | Sets output file name                  | `scraped_data.jsonl` |
| `threads(n)`     | Sets concurrent requests per domain    | `1`          |
| `speed(n)`       | Controls scraping speed (1-10)         | `5`          |
| `language("greek")` | Filters text by language (Greek only)  | `greek`      |

---

## 📜 License
This project is licensed under the MIT License.

---

## 👨‍💻 Author
**Charis Nikolaidis** – [GitHub](https://github.com/Charisn/Web-scraper) – ncharis97@gmail.com
---

### 🌟 Show Your Support!
Give a ⭐ if you like this project and find it useful!
