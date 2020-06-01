#!/bin/bash
import os
import re
import random
import requests
from bs4 import BeautifulSoup as Soup
from config import user_agents
from history import DownloadHistory, DownloadQueue
from config import conf


class HindiMp3Downloader:

    download_queue = DownloadQueue()
    download_history = DownloadHistory()

    def __init__(self):
        self.album_name = None
        self.album_link = None

    @staticmethod
    def get_response(url):
        choice = random.randint(0, 7)
        the_page = requests.get(url, headers={'User-Agent': user_agents[choice]})
        return the_page

    @staticmethod
    def make_soup(page):
        return Soup(page.text, 'html.parser')

    def parse_album_list(self):
        index = conf.read('host', 'index')
        page = self.get_response(url=index)
        soup = self.make_soup(page)
        for li in soup.find("section", {'class': 'primary'}).find_all('article'):
            title = li.find('a').text
            anchor = li.find('a', href=True)['href']
            self.download_queue.add(title, anchor)

    def process_album(self):
        page = self.get_response(url=self.album_link)
        soup = self.make_soup(page)
        self.album_name = soup.find('h1', {'class': 'post-title'}).text[:-11]

        for a in soup.find_all('tr')[1:]:
            td = a.find_all('td')[1:]

            # causing issue / list index out of range
            bit320 = str(td[1].a['href'])

            file_name = bit320.split('/')[-1:][0]
            extension = bit320.split('.')[-1:][0]
            title_search = re.findall('[A-Z]+[a-z]+', file_name)
            title = ' '.join(title_search[:-2])
            path = os.path.dirname(os.path.abspath(__file__)) + '/' + title
            os.makedirs(path, exist_ok=True)
            if extension not in ['zip', 'Zip', 'ZIP']:
                print("\t\tDownloading... {}".format(title))
                song = self.get_response(bit320)
                mp3 = open(path + '/' + title + '.' + extension, 'wb')
                mp3.write(song.content)
        self.download_history.add(key=self.album_name, value=self.album_link)


def main():
    sd = SongDownloader()
    url = "https://downloadming2.com/category/bollywood-mp3"
    resp = sd.get_response(url)
    soup = sd.make_soup(resp)
    dl_list = sd.get_album_link(soup)
    content = sd.download_list.readlines()
    for item in dl_list:
        if item not in content:
            print(f"Adding {item} to download queue")
            sd.download_list.write(f"{item}\n")
    print("Download queue ready")
    record_content = sd.records.readlines()
    print(record_content)
    for item in content:
        print(item)
        if item not in record_content:
            sd.download_album(item)
            # delete album from queue after download

        else:
            print(f"{item} already downloaded")


if __name__ == '__main__':
    main()
