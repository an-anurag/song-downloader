import requests
import random
from bs4 import BeautifulSoup as Soup


def get_response(url):

    # random integer to select user agent
    randomint = random.randint(0, 7)

    # User_Agents
    # This helps skirt a bit around servers that detect repeaded requests from the same machine.
    # This will not prevent your IP from getting banned but will help a bit by pretending to be different browsers
    # and operating systems.
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

    url = "https://downloadming.cool/category/bollywood-mp3"
    resp = get_response(url)
    my_soup = Soup(resp.text, 'html.parser')
    album_url_list = []
    for li in my_soup.find("section", {'class': 'primary'}).find_all('li'):
        anchor = li.find('a', href=True)['href']
        album_url_list.append(anchor)

    # test with one url
    top_album = album_url_list[0]
    resp = get_response(top_album)
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
            response = get_response(song_url_list[i])
            mp3 = open(song_name_list[i] + '.' + 'mp3', 'wb')
            mp3.write(response.content)
            i += 1
