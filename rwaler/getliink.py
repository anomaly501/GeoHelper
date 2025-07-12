# scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def scrape_and_save_links(url, output_file):
    """
    Scrapes all unique absolute links from a given URL and saves them to a text file.

    Args:
        url (str): The URL of the webpage to scrape.
        output_file (str): The path to the output text file.
    """
    print(f"[*] Fetching content from: {url}")
    
    try:
        # Use a user-agent to mimic a browser, which can help avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for bad status codes (like 404 or 500)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[!] Error: Could not fetch URL. {e}")
        return

    print("[*] Parsing HTML content...")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Use a set to automatically store only unique links
    unique_links = set()

    # Find all anchor tags <a> that have an 'href' attribute
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        # Use urljoin to convert relative URLs (like '/page.html') 
        # into absolute URLs (e.g., 'https://domain.com/page.html')
        absolute_link = urljoin(url, href)
        
        unique_links.add(absolute_link)

    if not unique_links:
        print("[!] No links were found on the page.")
        return

    # Sort the links alphabetically for a clean and ordered output
    sorted_links = sorted(list(unique_links))

    print(f"[*] Found {len(sorted_links)} unique links.")
    
    try:
        print(f"[*] Saving links to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for link in sorted_links:
                f.write(link + '\n')
        
        # Get the absolute path for the final confirmation message
        full_path = os.path.abspath(output_file)
        print(f"[+] Success! All links have been saved to: {full_path}")
        
    except IOError as e:
        print(f"[!] Error: Could not write to file. {e}")

if __name__ == "__main__":
    # Define the target URL and the output file name
    target_url = "https://geopandas.org/en/stable/docs/user_guide.html"
    output_filename = "scraped_links.txt"
    
    # Run the scraper
    scrape_and_save_links(target_url, output_filename)