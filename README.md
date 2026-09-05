# Scrapper (Sneha-162/Scrapper)

This repository (https://github.com/Sneha-162/Scrapper) is a small web-scraping project hosted on GitHub under the user `Sneha-162` and the repository name `Scrapper`.

Files in this repository

- web_scraper.ipynb — A Jupyter notebook that implements the scraper (data fetching, parsing, and export). Open this in Jupyter or VS Code and run the cells to reproduce the scraping steps.
- webpage.html — A sample HTML page included for local testing of the notebook's parsing logic.
- topics.csv — Example CSV data used by the notebook or produced by scraping; inspect it to see the expected output schema.
- scraper.py — A small, runnable script converted from the notebook that extracts topic titles, descriptions, and links and writes CSV/JSON.
- requirements.txt — Pinned dependencies for reproducible installs.
- pyvenv.cfg and Scripts/ — These come from a Python virtual environment. They are not needed in the repository and are covered by .gitignore.

Repository link

- GitHub: https://github.com/Sneha-162/Scrapper

What you can do with this repo

- Reproduce the notebook locally: install Jupyter, open web_scraper.ipynb, and run the cells. The notebook contains code and inline explanations to demonstrate how pages are fetched and parsed.
- Run the script directly: `scraper.py` is a small CLI wrapper around the same parsing logic used in the notebook and works with either a live URL or the included `webpage.html` for offline testing.
- Inspect or extend `topics.csv` to see the scraped fields and their ordering.

Quick start (recommended)

1. Clone the repository and create a virtual environment:

   git clone https://github.com/Sneha-162/Scrapper.git
   cd Scrapper
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate    # Windows

2. Install pinned dependencies:

   pip install -r requirements.txt

3. Run the sample scraper on the included local HTML (no network required):

   python scraper.py --input webpage.html --output topics.csv --format csv

4. Or run the scraper against the live GitHub Topics page:

   python scraper.py --input https://github.com/topics --output topics.csv --format csv

CLI usage (scraper.py)

A small command-line wrapper is provided in `scraper.py` (converted from the notebook).

Options

- -i, --input: URL or local HTML file (default: https://github.com/topics)
- -o, --output: Output path (default: topics.csv)
- -f, --format: Output format: csv or json (default: csv)
- --save-html: Save fetched page to webpage.html (useful when debugging)
- --rate: Rate limit delay (seconds) between requests
- --user-agent: Custom User-Agent header

Examples

  # Fetch live GitHub Topics and write CSV
  python scraper.py --input https://github.com/topics --output topics.csv --format csv

  # Parse the included sample HTML and write JSON
  python scraper.py --input webpage.html --output topics.json --format json

  # Save the fetched HTML to webpage.html for debugging
  python scraper.py --input https://github.com/topics --save-html

Notes

- The script uses requests + BeautifulSoup and contains a simple retry/backoff strategy for robustness. If the page structure changes, update the selectors in `scraper.py` (there are clear constants at the top of the file).
- For reproducible installs, use the pinned `requirements.txt` in the repo.
- The repository includes a simple pytest-based test and a GitHub Actions workflow that runs the tests against the included `webpage.html` (no external network calls during CI).

Development suggestions

- Remove the embedded virtualenv files from history if you want to shrink the repository size (I added .gitignore so future commits won't re-add them).
- Consider adding a LICENSE if you want to make the project explicitly open-source.
- If you want the notebook converted to a more feature-rich script (concurrency, headless browsing for JS-heavy pages), I can help with that next.

Contact / Issues

If you find bugs or want enhancements, open an issue in the repository: https://github.com/Sneha-162/Scrapper/issues
