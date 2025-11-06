# Web Scraping with AI Summarization

This project is a web scraping tool that searches DuckDuckGo for a given query, scrapes the search results, and uses OpenAI's GPT-3.5 to generate summaries of the web pages.

## Features

- Search DuckDuckGo for any query
- Automated web scraping using Selenium and BeautifulSoup4
- Page content extraction and storage
- AI-powered summarization using OpenAI's GPT-3.5-turbo
- Results saved in JSON format
- Headless browser operation
- Error handling and graceful termination

## Prerequisites

- Python 3.x
- Google Chrome browser
- OpenAI API key

## Required Python Packages

- selenium
- beautifulsoup4
- requests
- openai
- webdriver-manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tbharathraj205/web-scraping.git
cd web-scraping
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install selenium beautifulsoup4 requests openai webdriver-manager
```

4. Set up your OpenAI API key:
```bash
# On openai_api.py upadte the code
api_key = "your-api-key-here"
```

## Usage

1. Run the script:
```bash
python web-scraper.py
```

2. Enter your search query when prompted.

3. The program will:
	 - Search DuckDuckGo for your query
	 - Extract relevant links
	 - Visit each webpage
	 - Extract the content
	 - Generate an AI summary
	 - Save everything to `articles.json`

## Output Format

The results are saved in `articles.json` with the following structure:
```json
[
	{
		"url": "https://example.com",
		"status": 200,
		"content": "HTML content of the page",
		"summary": "AI-generated summary of the page"
	}
]
```

## Files Description

- `web-scraper.py`: Main script that handles web scraping and coordination
- `openai_api.py`: Handles AI summarization using OpenAI's API
- `articles.json`: Output file containing scraped data and summaries

## Error Handling

The program includes error handling for:
- Network issues
- Invalid URLs
- Missing API keys
- Page load timeouts
- Scraping failures
- API rate limits

## Important Notes

- Respect websites' robots.txt and terms of service
- Be mindful of rate limits for both web scraping and API calls
- Keep your API keys secure and never commit them to source control
- The program uses a headless browser to minimize resource usage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security

Never share or commit your API keys. Always use environment variables for sensitive data.
