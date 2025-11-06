from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import requests
import signal
import sys
import openai_api as page
 # Direct import

# Global variable to store the WebDriver instance
driver = None

def signal_handler(signum, frame):
    print("\nReceived interrupt signal. Cleaning up...")
    if driver:
        driver.quit()
    sys.exit(0)

# Set up signal handler
signal.signal(signal.SIGINT, signal_handler)

def scrape(url):
    global driver
    try:
        if not driver:
            print("Initializing Chrome WebDriver...")
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Wait for elements to load with timeout
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Additional wait for dynamic content
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
        
        return links
        
    except TimeoutException:
        print("Timeout waiting for page to load")
        return []
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    finally:
        driver.quit()


def scrape_page(links):
    if not links:
        print("No links to process")
        return []

    http_links = [
        link for link in links 
        if link.startswith("http") and "duck" not in link.lower()
    ]

    if not http_links:
        print("No valid HTTP links found")
        return []

    unique_links = sorted(set(http_links))
    print(f"Processing {len(unique_links)} unique links...")
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

    for link in unique_links:
        try:
            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            soup = BeautifulSoup(response.text, "html.parser")

            body_tag = soup.find("body")

            if body_tag:
                content = body_tag.decode_contents()
                # Get summary using OpenAI
                try:
                    summary = page.run_query(link)
                except Exception as e:
                    print(f"Summary generation failed for {link}: {str(e)}")
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

            print(f"Processed {link}")
            results.append(result)

        except requests.RequestException as e:
            results.append({
                "url": link,
                "status": getattr(e.response, 'status_code', 500),
                "error": str(e),
                "summary": None
            })

    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("Saved all webpage HTML to articles.json")



def query():
    try:
        print("Starting web scraping process...")
        query = input("Enter your search query: ")
        formatted_query = query.replace(" ", "+")
        url = f"https://duckduckgo.com/?q={formatted_query}&ia=web"
        print(f"Searching DuckDuckGo for: {query}")

        print("Scraping search results...")
        links = scrape(url)
        if links:
            print(f"Found {len(links)} links")
            print("Scraping individual pages...")
            scrape_page(links)
        else:
            print("No links found in the search results")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    query()