  # FastAPI Scraper - Web Search & Summarization API

A lightweight FastAPI-based web scraping and summarization service that searches DuckDuckGo and generates intelligent summaries of web pages. Designed for containerized deployment with Docker.

## 🚀 Features

- **DuckDuckGo Search Integration**: Search the web using the DDGS library
- **Intelligent Text Summarization**: Extracts key sentences using word frequency scoring
- **RESTful API**: FastAPI-powered endpoints with API key authentication
- **Docker-Native**: Built for containerized deployment
- **Batch Processing**: Scrapes and summarizes multiple results in one go
- **JSON Export**: Saves all results to structured JSON files

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Output Format](#output-format)
- [Troubleshooting](#troubleshooting)

## 📁 Project Structure

```
fastapi-scraper/
│
├── main.py              # Core scraping and orchestration logic
├── summarize.py         # Text summarization algorithm
├── server.py            # FastAPI server with authentication
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
├── .dockerignore        # Docker build exclusions
└── summarize.json       # Output file (generated at runtime)
```

## 🔧 Requirements

- Docker 20.10+
- Docker Compose (optional)

**No Python installation required** - everything runs in Docker!

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd fastapi-scraper
```

### 2. Build the Docker Image

```bash
docker build --no-cache -t fastapi-scraper:latest .
```

### 3. Run the Container

```bash
docker run --rm -p 8000:8000 fastapi-scraper:latest
```

### 4. Test the API

```bash
curl -X GET "http://localhost:8000/search?query=python&max_results=3" \
     -H "key: mysecret123"
```

Visit **http://localhost:8000/docs** for interactive API documentation.

## 🐳 Docker Deployment

### Basic Deployment

**Build the image:**
```bash
docker build --no-cache -t fastapi-scraper:latest .
```

**Run with automatic cleanup:**
```bash
docker run --rm -p 8000:8000 fastapi-scraper:latest
```

**Run in detached mode:**
```bash
docker run -d --name scraper-api -p 8000:8000 fastapi-scraper:latest
```

## 📡 API Documentation

### Endpoint: `/search`

**Method:** `GET`

**Headers:**
- `key` (required): API authentication key (default: `mysecret123`)

**Query Parameters:**
- `query` (required): Search query string
- `max_results` (optional): Number of results to fetch (default: 5)

**Example Request:**

```bash
curl -X GET "http://localhost:8000/search?query=cybersecurity%20trends&max_results=5" \
     -H "key: mysecret123"
```

**Python Example:**

```python
import requests

headers = {"key": "mysecret123"}
params = {
    "query": "web scraping tools",
    "max_results": 3
}

response = requests.get("http://localhost:8000/search", 
                       headers=headers, 
                       params=params)
print(response.json())
```

**Response Format:**

```json
[
  {
    "url": "https://example.com/article",
    "status": 200,
    "summary": "This is an intelligent summary of the webpage content..."
  },
  {
    "url": "https://example2.com/page",
    "status": 200,
    "summary": "Another summarized content..."
  }
]
```

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| 401 | Invalid API key |
| 422 | Missing required parameters |
| 500 | Internal server error |

### Interactive Documentation

Once the container is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ⚙️ Configuration

### Change API Key

**Option 1: Environment Variable (Recommended)**

```bash
docker run --rm -p 8000:8000 -e API_KEY=your-secure-key fastapi-scraper:latest
```

Update `server.py` to read from environment:

```python
import os
API_KEY = os.getenv("API_KEY", "mysecret123")
```

**Option 2: Edit Source Code**

Edit `server.py`:

```python
API_KEY = "your-secure-api-key-here"
```

Then rebuild:
```bash
docker build --no-cache -t fastapi-scraper:latest .
```

### Modify Summarization Settings

Edit `summarize.py`:

```python
def summarize_text(text, max_sentences=6):  # Change to 3, 8, etc.
    # ... rest of the code
```

Rebuild after changes:
```bash
docker build --no-cache -t fastapi-scraper:latest .
```

### Custom User-Agent

Edit `main.py` in the `scrape_page()` function:

```python
headers = {
    "User-Agent": "FastAPI-Scraper/1.0 (+https://yoursite.com/bot)",
    # ... other headers
}
```

## 📤 Output Format

Results are saved to `summarize.json` inside the container:

```json
[
  {
    "url": "https://example.com",
    "status": 200,
    "summary": "Extracted summary text..."
  },
  {
    "url": "https://failed-site.com",
    "status": 500,
    "error": "Connection timeout",
    "summary": null
  }
]
```

**Fields:**
- `url`: The webpage URL
- `status`: HTTP status code
- `summary`: Generated summary (null on failure)
- `error`: Error message (only present on failures)

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**

```bash
# Check what's using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Use a different port
docker run --rm -p 8080:8000 fastapi-scraper:latest
```

**2. Docker Build Fails**

```bash
# Clear Docker cache and rebuild
docker system prune -a
docker build --no-cache -t fastapi-scraper:latest .
```

**3. Container Exits Immediately**

```bash
# Check logs for errors
docker logs scraper-api

# Run in interactive mode to debug
docker run --rm -it fastapi-scraper:latest /bin/bash
```

**4. API Returns 401 Unauthorized**

- Verify the `key` header matches the API_KEY in `server.py`
- Check header format: `-H "key: mysecret123"` (not `"api-key"`)

**5. Empty Search Results**

- DuckDuckGo may be rate-limiting; add delays between requests
- Verify container has internet access: `docker run --rm fastapi-scraper:latest curl -I https://duckduckgo.com`
- Try a different search query

**6. Image Build is Slow**

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t fastapi-scraper:latest .
```





## 📝 License

[Specify your license here, e.g., MIT, Apache 2.0]

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Test in Docker: `docker build -t test . && docker run --rm test`
4. Commit changes (`git commit -am 'Add feature'`)
5. Push and open a Pull Request

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing issues for solutions

---

**Built using FastAPI, Docker, DuckDuckGo Search, and BeautifulSoup**

