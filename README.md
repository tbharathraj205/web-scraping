# Web Article Scraper & Summarizer

A script that searches the web, collects article links, extracts text, and summarizes the information using the OpenAI API. All results are saved into a structured JSON file.

## ✨ How It Works

1. You enter a search term.

2. The script finds related web pages (via DuckDuckGo).

3. Text content is extracted from each page.

4. AI generates a clear, short summary.

5. Everything is saved to articles.json.

## 🚀 Features

- Web search using DuckDuckGo (ddgs)

- Automatic webpage text extraction with BeautifulSoup

- AI summaries generated using OpenAI

- Avoids duplicates and skips unreadable pages

- Saves results in clean JSON format

## 📂 Project Structure
```
project-folder/
│
├── main.py           # Orchestrates search + scraping + summarization
├── summarize.py      # Handles text extraction + OpenAI summary generation
└── articles.json     # Output file created after running the script
```
🔧 Installation

Install required dependencies:

```
pip install ddgs requests beautifulsoup4 openai
```

### 🔑 API Key Setup

Open summarize.py and set your OpenAI API key:
```
openai.api_key = "your_api_key_here"

```
## ▶️ Usage

Run the script:
```
python main.py
```

You'll be prompted for:
```
Enter your search query:
How many results? (default 10):
```

Example:
```
Enter your search query: climate change news
How many results? (default 10): 5

```
The script will then:

- Search DuckDuckGo

- Extract article text

- Summarize each article

- Save everything into summarize.json

📝 Output Example (summarize.json)
```
[
  {
    "url": "https://example.com/article",
    "status": 200,
    "summary": "This article discusses the impact of climate change..."
  }
]
```

## ⚠ Notes

Some websites may block scraping or have unreadable content — these are automatically skipped.

Default summarization model is gpt-3.5-turbo. You can change the model in summarize.py.

