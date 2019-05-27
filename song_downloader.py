import requests
import random
from bs4 import BeautifulSoup as Soup
import re


def get_response(url):

    randomint = random.randint(0, 7)

    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
    ]

    the_page = requests.get(url, headers={'User-Agent': user_agents[randomint]})
    return the_page


if __name__ == '__main__':

    album_urls = [x for x in open('download_list.txt', 'r')]

    for url in album_urls:
        resp = get_response(url[:-1])
        soup = Soup(resp.text, 'html.parser')
        for a in soup.find_all('tr')[1:]:
            td = a.find_all('td')[1:]
            bit320 = str(td[1].a['href'])
            extension = bit320.split('.')[-1:][0]
            file_name = bit320.split('/')[-1:][0]
            title_search = re.findall('[A-Z]+[a-z]+', file_name)
            title_extract = [x for x in title_search if x != "Downloadming" and x != "Kbps"]
            title = ' '.join(title_extract)
            song = get_response(bit320)
            print("Downloading... {}".format(title))
            mp3 = open(title + '.' + extension, 'wb')
            mp3.write(song.content)
