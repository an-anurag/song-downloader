import requests
from urllib import request
from bs4 import BeautifulSoup as Soup
url = "https://downloadming.cool/category/bollywood-mp3"
resp = requests.get(url)
my_soup = Soup(resp.text, 'html.parser')
album_url_list = []
# add support for page changes monitoring
for li in my_soup.find("section", {'class': 'primary'}).find_all('li'):
    anchor = li.find('a', href=True)['href']
    album_url_list.append(anchor)

# test with one url
bharat = album_url_list[0]
resp = requests.get(bharat)
soup = Soup(resp.text, 'html.parser')
song_url_list = []
song_name_list = []
for i in soup.find('table').find_all('tr')[1:]:
    song_name = str(i.find('td').text)[5:]
    song_name_list.append(song_name)
    song_url = i.contents[2].a['href']
    song_url_list.append(song_url)
    extension = str(song_url.split('.')[-1:])

# add support for ZIP file if it exist
if len(song_url_list[:-1]) == len(song_name_list[:-1]):
    i = 0
    while i < len(song_url_list):
        print(f'Downloading...{song_name_list[i]}')
        response = requests.get(song_url_list[i])
        mp3 = open(song_name_list[i] + '.' + 'mp3', 'wb')
        mp3.write(response.content)
        i += 1
