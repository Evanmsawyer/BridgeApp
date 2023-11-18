import requests
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def download_file(url):
    subfolder = 'linfiles'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    base_filename = os.path.splitext(url.split('/')[-1])[0] + '.lin'
    local_filename = os.path.join(subfolder, base_filename)
    counter = 1
    original_filename = local_filename
    while os.path.exists(local_filename):
        local_filename = os.path.splitext(original_filename)[0] + '-' + str(counter) + '.lin'
        counter += 1
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename


def is_valid_link(href, root_url):
    if not href or '../' in href or href.startswith('mailto:') or href.startswith('MAILTO:'):
        return False
    full_url = urljoin(root_url, href)
    parsed_url = urlparse(full_url)
    return parsed_url.scheme in ['http', 'https'] and \
           parsed_url.netloc == urlparse(root_url).netloc

def crawl(url, root_url, visited):
    if url in visited:
        return
    visited.add(url)

    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"Skipping {url}: Status code {r.status_code}")
            return

        soup = BeautifulSoup(r.content, 'html.parser')
        print(f"Visiting: {url}")  

        for link in soup.find_all('a'):
            href = link.get('href')
            if is_valid_link(href, root_url):
                full_url = urljoin(url, href)
                print(f"Found link: {full_url}") 
                if full_url.endswith('.lin'):
                    download_file(full_url)
                elif full_url not in visited:
                    crawl(full_url, root_url, visited)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing {url}: {e}")

visited_urls = set()
root_url = 'http://www.sarantakos.com/bridge/vugraph'  
crawl(root_url, root_url, visited_urls)
