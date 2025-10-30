import os
from openai import OpenAI

def run_query(link):
    """
    Summarize a webpage using OpenAI's API.
    
    Args:
        link (str): URL of the webpage to summarize
        
    Returns:
        str: Summarized text or error message
    """
    try:
        # Embed your API key directly here
        api_key = 'your-api-key-here'
        if not api_key:
            raise ValueError("OPENAI_API_KEY error: API key is missing.")
            
        client = OpenAI(api_key=api_key)
        
        # Send query with proper spacing
        prompt = f"Summarize the following webpage: {link}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes web pages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Limit summary length
        )
        
        summary = response.choices[0].message.content
        print(f"Summary for {link}:\n{summary}\n")
        return summary
        
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    # Test with a sample URL
    test_url = "https://example.com"
    run_query(test_url)