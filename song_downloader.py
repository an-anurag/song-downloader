import re
from bs4 import BeautifulSoup as Soup
from page_change import get_response

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
