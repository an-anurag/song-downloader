#!/bin/bash
import os
import re
import random
import requests
from bs4 import BeautifulSoup as Soup
from config import user_agents


class SongDownloader:

    def __init__(self):
        self.url = ""

    def get_response(self, url):
        randomint = random.randint(0, 7)
        the_page = requests.get(url, headers={'User-Agent': user_agents[randomint]})
        return the_page

    def make_soup(self, page):
        return Soup(page.text, 'html.parser')

    def get_album_name(self, soup):
        name = soup.find('h1', {'class': 'post-title'}).text
        name = name[:-11]
        return name

    def make_dir(self, path, name):
        return os.makedirs(path + str('/' + name), exist_ok=True)

    def get_album_link(self, soup):
        live_album_urls = []
        for li in soup.find("section", {'class': 'primary'}).find_all('article'):
            anchor = li.find('a', href=True)['href']
            name = li.find('a', href=True)
            album_name = name.text[:-11]
            live_album_urls.append(anchor)
        return live_album_urls

    def write_dl_list(self, dl_list):
        with open('download_list.txt', 'a') as dl_file:
            for link in dl_list:
                dl_file.write(f"{link}\n")

    def read_dl_list(self):
        return [x for x in open('download_list.txt', 'r')]

    def add_to_records(self, album, flag=True):
        records = open('album_records.txt', 'a')
        if flag:
            records.write(f"{album}")
            records.close()

    def download_album(self):
        dl_list = self.read_dl_list()
        records = open('album_records.txt', 'r')
        for url in dl_list:
            is_written = False
            resp = sd.get_response(url[:-1])
            soup = sd.make_soup(resp)
            for a in soup.find_all('tr')[1:]:
                td = a.find_all('td')[1:]
                bit320 = str(td[1].a['href'])
                extension = bit320.split('.')[-1:][0]
                file_name = bit320.split('/')[-1:][0]
                title_search = re.findall('[A-Z]+[a-z]+', file_name)
                title_extract = [x for x in title_search if x != "Downloadming" and x != "Kbps"]
                title = ' '.join(title_extract)
                song = sd.get_response(bit320)
                print("Downloading... {}".format(title))
                album_name = sd.get_album_name(soup)
                path = os.path.dirname(os.path.abspath(__file__)) + '/' + album_name
                os.makedirs(path, exist_ok=True)
                mp3 = open(path + '/' + title + '.' + extension, 'wb')
                mp3.write(song.content)
            is_written = True
            self.add_to_records(url, is_written)


if __name__ == '__main__':
    sd = SongDownloader()
    url = "https://downloadming.cool/category/bollywood-mp3"
    resp = sd.get_response(url)
    soup = sd.make_soup(resp)
    dl_list = sd.get_album_link(soup)
    sd.write_dl_list(dl_list)
    sd.download_album()
    # TODO: handle repeated downloading of same album
    # TODO: clear completed download list
    # TODO: if zip album found download it and extract it dont download the tracks
