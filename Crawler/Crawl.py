import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_site(base_url, max_pages=20):
    visited, to_visit, texts = set(), [base_url], []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Extract text
            page_text = " ".join([p.get_text() for p in soup.find_all("p")])
            texts.append({"url": url, "text": page_text})

            # Find links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(base_url, link["href"])
                if base_url in full_url and full_url not in visited:
                    to_visit.append(full_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    return texts