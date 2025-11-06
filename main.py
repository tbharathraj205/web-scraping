from ddgs import DDGS
import json
import requests
from bs4 import BeautifulSoup
import signal
import sys
import summarize as page

def signal_handler(signum, frame):
    print("\nReceived interrupt signal. Cleaning up...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def scrape(query, max_results=10):
    """Search DuckDuckGo using DDGS library"""
    try:
        print(f"Searching DuckDuckGo using DDGS library...")
        
        # Initialize DDGS and perform search
        results = DDGS().text(query, region='us-en', safesearch='moderate', max_results=max_results)
        
        links = []
        for result in results:
            url = result.get('href')
            if url:
                links.append(url)
                print(f"Found: {url}")
        
        return links
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return []

def scrape_page(links):
    if not links:
        print("No links to process")
        return []

    unique_links = sorted(set(links))
    print(f"\nProcessing {len(unique_links)} unique links...")
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    for idx, link in enumerate(unique_links, 1):
        try:
            print(f"\n[{idx}/{len(unique_links)}] Fetching: {link}")
            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            body_tag = soup.find("body")

            if body_tag:
                try:
                    print(f"Generating summary...")
                    summary = page.run_query(link)
                except Exception as e:
                    print(f"Summary generation failed: {str(e)}")
                    summary = None
                    
                result = {
                    "url": link,
                    "status": response.status_code,
                    "summary": summary
                }
            else:
                result = {
                    "url": link,
                    "status": 404,
                    "summary": None
                }

            print(f"✓ Processed successfully")
            results.append(result)

        except requests.RequestException as e:
            print(f"✗ Failed: {str(e)}")
            results.append({
                "url": link,
                "status": getattr(e.response, 'status_code', 500),
                "error": str(e),
                "summary": None
            })

    with open("summarize.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"\n✓ Saved all webpage data to summarize.json")
    return results

def query():
    try:
        print("Starting web scraping process...")
        search_query = input("Enter your search query: ")
        max_results_input = input("How many results? (default 10): ")
        max_results = int(max_results_input) if max_results_input else 10
        
        print(f"Searching for: {search_query}\n")
        links = scrape(search_query, max_results)
        
        if links:
            print(f"\n✓ Found {len(links)} valid links")
            print("\nScraping individual pages...")
            scrape_page(links)
        else:
            print("\n✗ No links found in the search results")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"\n✗ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    query()
