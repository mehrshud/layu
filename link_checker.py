
import requests
from bs4 import BeautifulSoup

def check_links(html_file):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        links = soup.find_all('a')
        broken_links = []
        for link in links:
            href = link.get('href')
            if href:
                try:
                    response = requests.head(href)
                    if response.status_code >= 400:
                        broken_links.append(href)
                except requests.exceptions.RequestException:
                    broken_links.append(href)
        return broken_links

def fix_broken_links(html_file, broken_links):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href in broken_links:
                link['href'] = '#'
        with open(html_file, 'w') as f:
            f.write(str(soup))

def main():
    html_files = ['index.html', 'our-path.html']
    for html_file in html_files:
        broken_links = check_links(html_file)
        if broken_links:
            print(f'Broken links found in {html_file}: {broken_links}')
            fix_broken_links(html_file, broken_links)
        else:
            print(f'No broken links found in {html_file}')

if __name__ == '__main__':
    main()
