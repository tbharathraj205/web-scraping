import openai
import requests
from bs4 import BeautifulSoup
import os

# Set your OpenAI API key
openai.api_key = ""

def extract_text_from_url(url):
    """Extract main text content from a URL"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text from paragraphs
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        
        # If no paragraphs found, get all text
        if not article_text.strip():
            article_text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in article_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        article_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return article_text
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def chunk_text(text, max_tokens=3000):
    """Split text into chunks that fit within token limits"""
    # Rough estimate: 1 token ≈ 4 characters
    max_chars = max_tokens * 4
    
    if len(text) <= max_chars:
        return [text]
    
    # Split into sentences
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def summarize_text(text):
    """Summarize text using OpenAI API"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates concise, informative summaries of content. Focus on the key facts, main points, and important details."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following article:\n\n{text}"
                }
            ],
            max_tokens=500,
            temperature=0.5
        )
        
        summary = response.choices[0].message.content
        return summary
        
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None

def run_query(url):
    """Main function to extract and summarize webpage content"""
    print(f"Extracting content from: {url}")
    
    # Extract text from URL
    text = extract_text_from_url(url)
    
    if not text:
        return "Failed to extract content from the URL."
    
    # Limit text length for API call
    if len(text) > 12000:  # Roughly 3000 tokens
        text = text[:12000]
    
    print(f"Extracted {len(text)} characters, generating summary...")
    
    # Generate summary
    summary = summarize_text(text)
    
    if summary:
        return summary
    else:
        return "Failed to generate summary."

# Alternative function for handling very long articles
def run_query_long(url):
    """Handle very long articles by chunking and summarizing"""
    print(f"Extracting content from: {url}")
    
    text = extract_text_from_url(url)
    
    if not text:
        return "Failed to extract content from the URL."
    
    # Split into chunks
    chunks = chunk_text(text, max_tokens=3000)
    
    if len(chunks) == 1:
        return summarize_text(chunks[0])
    
    print(f"Processing {len(chunks)} chunks...")
    
    # Summarize each chunk
    chunk_summaries = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Summarizing chunk {i}/{len(chunks)}...")
        summary = summarize_text(chunk)
        if summary:
            chunk_summaries.append(summary)
    
    # Combine and summarize the summaries
    combined = " ".join(chunk_summaries)
    
    print("Generating final summary...")
    final_summary = summarize_text(combined)
    
    return final_summary if final_summary else "Failed to generate summary."
