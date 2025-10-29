from selenium import webdriver
from bs4 import BeautifulSoup
import time

def scrape(url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(3)  # wait for JS to load
    soup = BeautifulSoup(driver.page_source, "html.parser")

    links = [a['href'] for a in soup.find_all('a', href=True)]
    driver.quit()

    return links


def save_http_links(links, filename="http_links.txt"):
    """Save only unique HTTP/HTTPS links that do NOT contain 'duck'."""
    
    # Keep only http/https links and remove any containing 'duck'
    http_links = [
        link for link in links
        if link.startswith("http") and "duck" not in link.lower()
    ]

    # Remove duplicates
    unique_links = sorted(set(http_links))

    # Save to file
    with open(filename, "w", encoding="utf-8") as file:
        for link in unique_links:
            file.write(link + "\n")

    print(f"✅ Saved {len(unique_links)} unique HTTP/HTTPS links to '{filename}'")



def query():
    # Ask the user for a search query
    query = input("Enter your search query: ")

    # Replace spaces with '+' to make it URL-friendly
    formatted_query = query.replace(" ", "+")

    # Create the DuckDuckGo search URL
    url = f"https://duckduckgo.com/?q={formatted_query}&ia=web"

    print("Your DuckDuckGo search URL is:")
    print(url)

    # Scrape and save
    links = scrape(url)
    save_http_links(links)


if __name__ == "__main__":
    query()
