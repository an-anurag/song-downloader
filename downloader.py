#!/bin/bash
import os
import re
import random
import requests
from bs4 import BeautifulSoup as Soup
from config import user_agents


class SongDownloader:

    def __init__(self):
        self.records = open('album_records.txt', 'a+')
        self.download_list = open('download_list.txt', 'r+')

    @staticmethod
    def get_response(url):
        choice = random.randint(0, 7)
        the_page = requests.get(url, headers={'User-Agent': user_agents[choice]})
        return the_page

    @staticmethod
    def make_soup(page):
        return Soup(page.text, 'html.parser')

    @staticmethod
    def get_album_name(soup):
        name = soup.find('h1', {'class': 'post-title'}).text[:-11]
        return name

    @staticmethod
    def get_album_link(soup):
        live_album_urls = []
        for li in soup.find("section", {'class': 'primary'}).find_all('article'):
            anchor = li.find('a', href=True)['href']
            live_album_urls.append(anchor)
        return live_album_urls

    def add_to_records(self, album, flag):
        if flag:
            self.records.write(f"{album}\n")
            self.records.close()

    def download_album(self, link):
        resp = self.get_response(link)
        soup = self.make_soup(resp)
        album_name = self.get_album_name(soup)
        print("ALBUM: %s" % album_name)
        for a in soup.find_all('tr')[1:]:
            td = a.find_all('td')[1:]
            bit320 = str(td[1].a['href'])
            file_name = bit320.split('/')[-1:][0]
            extension = bit320.split('.')[-1:][0]
            title_search = re.findall('[A-Z]+[a-z]+', file_name)
            title = ' '.join(title_search[:-2])
            path = os.path.dirname(os.path.abspath(__file__)) + '/' + album_name
            os.makedirs(path, exist_ok=True)
            if extension not in ['zip', 'Zip', 'ZIP']:
                print("\t\tDownloading... {}".format(title))
                song = self.get_response(bit320)
                mp3 = open(path + '/' + title + '.' + extension, 'wb')
                mp3.write(song.content)
        is_written = True
        self.add_to_records(link, is_written)


def main():
    sd = SongDownloader()
    url = "https://downloadming2.com/category/bollywood-mp3"
    resp = sd.get_response(url)
    soup = sd.make_soup(resp)
    dl_list = sd.get_album_link(soup)
    content = sd.download_list.read().split('\n')
    for item in dl_list:
        if item not in content:
            print(f"Adding {item} to download queue")
            sd.download_list.write(f"{item}\n")
    print("Download queue ready")
    record_content = sd.records.read().split('\n')
    for item in content:
        if item not in record_content:
            sd.download_album(item)
        else:
            print(f"{item} already downloaded")


if __name__ == '__main__':
    main()
