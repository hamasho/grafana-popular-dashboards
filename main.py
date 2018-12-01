import base64
import os.path
import re
from bs4 import BeautifulSoup
import requests


def get_url(url):
    print('get_url: {}'.format(url))
    file_name = base64.b64encode(bytes(url, 'utf-8'))
    file_name = file_name.decode('utf-8')
    path = '/tmp/{}'.format(file_name)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    print('start download: {}'.format(url))
    response = requests.get(url)
    with open(path, 'w') as f:
        f.write(response.text)
    return response.text


def get_list(index=1):
    url = 'https://grafana.com/dashboards?page={}'.format(index)
    html_doc = get_url(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    a_list = soup.find_all('a', 'list__itemContent')
    result = []
    for a_elm in a_list:
        downloads = int(re.search(r'\d+', a_elm.find('h5').text).group(0))
        title = a_elm.find('span', 'list__itemName').text
        href = a_elm['href']
        item = (downloads, title, href)
        result.append(item)
    return result


def main():
    results = []
    for i in range(1, 15):
        results += get_list(index=i)
    results = sorted(results, key=lambda item: item[0], reverse=True)
    for idx, item in enumerate(results[:100]):
        downloads, title, href = item
        print('{}: [{} ({} downloads)](https://grafana.com{})'.format(
            idx + 1, title, downloads, href,
        ))


if __name__ == "__main__":
    main()
