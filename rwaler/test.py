# extract_data.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import time
import re

def read_links_from_file(filepath):
    """Reads a list of URLs from a text file."""
    if not os.path.exists(filepath):
        print(f"[!] Error: Input file '{filepath}' not found.")
        print("Please run the first script to generate 'scraped_links.txt' first.")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        # Read lines and strip any whitespace
        links = [line.strip() for line in f if line.strip()]
    return links

def sanitize_url_to_filename(url):
    """Converts a URL into a safe, valid filename."""
    # Parse the URL to get the path
    parsed_url = urlparse(url)
    
    # Start with the domain, replacing dots with underscores
    filename = parsed_url.netloc.replace('.', '_')
    
    # Add the path, replacing slashes and other invalid characters
    # This regex removes most characters that are invalid in filenames
    path_safe = re.sub(r'[\\/*?:"<>|]', "_", parsed_url.path)
    
    # Remove leading slash if it exists
    if path_safe.startswith('/'):
        path_safe = path_safe[1:]
        
    filename = os.path.join(filename, path_safe)
    
    # If the path ends in a slash, name it index.html
    if filename.endswith('_'):
        filename += 'index.html'

    return filename + ".txt"

def scrape_content_from_url(url, session):
    """
    Scrapes the main content from a single URL.
    The main content is assumed to be in a div with class 'bd-content'.
    """
    try:
        # Using a session object for potential connection pooling
        response = session.get(url, timeout=15)
        response.raise_for_status()

        # --- IMPORTANT: Check if the content is HTML before parsing ---
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print(f"    - Skipping non-HTML content: {url} ({content_type})")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Target the specific main content area ---
        main_content_div = soup.find('div', class_='bd-content')

        if main_content_div:
            # Get text and clean it up
            text = main_content_div.get_text(separator='\n', strip=True)
            
            # Clean up excessive blank lines for better readability
            cleaned_text = re.sub(r'\n\s*\n', '\n\n', text)
            return cleaned_text
        else:
            # Handle cases where the main content div isn't found
            print(f"    - Could not find main content <div class='bd-content'> on {url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"    - Error fetching {url}: {e}")
        return None

def main():
    """
    Main function to orchestrate the scraping process.
    """
    input_file = "scraped_links.txt"
    output_dir = "scraped_content"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Content will be saved in the '{output_dir}/' directory.")

    links_to_scrape = read_links_from_file(input_file)
    if not links_to_scrape:
        return

    total_links = len(links_to_scrape)
    print(f"[*] Found {total_links} links to process.")
    
    # Use a requests Session for performance improvements
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)

    for i, link in enumerate(links_to_scrape):
        print(f"\n[{i+1}/{total_links}] Processing: {link}")

        # Scrape the content from the link
        content = scrape_content_from_url(link, session)

        if content:
            # Create a safe filename from the URL
            output_filename = sanitize_url_to_filename(link)
            # Create subdirectory structure within the main output directory
            full_output_path = os.path.join(output_dir, output_filename)
            os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
            
            try:
                with open(full_output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"    + Success! Content saved to {full_output_path}")
            except IOError as e:
                print(f"    - Error writing to file {full_output_path}: {e}")
        
        # --- Be a polite scraper: wait a bit between requests ---
        time.sleep(1) 

    print("\n[+] All tasks complete.")

if __name__ == "__main__":
    main()