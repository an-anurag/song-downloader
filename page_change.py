import os
import random
import smtplib
import requests
from bs4 import BeautifulSoup as Soup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
    # scrape letest album list
    url = "https://downloadming.cool/category/bollywood-mp3"
    resp = get_response(url)
    my_soup = Soup(resp.text, 'html.parser')
    live_album_urls = []
    for li in my_soup.find("section", {'class': 'primary'}).find_all('li'):
        anchor = li.find('a', href=True)['href']
        live_album_urls.append(anchor)

    directory = os.path.dirname(os.path.abspath(__file__))
    read_file = open(directory + '/album_records.txt', 'r')
    last_line = read_file.readlines()[-1:]
    pattern = re.compile("Top album:\s+\S+")
    old_top_album = re.search(pattern, last_line[0])
    old_top_album = old_top_album.group()
    old_top_album = old_top_album[11:]
    read_file.close()
    updated_album_urls = []
    search_old_top_album = [s for s in live_album_urls if old_top_album in s]
    old_top_album_index = live_album_urls.index(search_old_top_album[0])
    if not old_top_album_index == 0:
        updated_album_urls.append(live_album_urls[:old_top_album_index])
        download_list = open(directory + '/download_list.txt', 'w')
        for album in updated_album_urls[0]:
            album_info = "{}\n".format(album)
            download_list.writelines(album_info)
        me = 'an.anuraag@gmail.com'
        you = 'an.anurag@live.in'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Song downloader update'
        msg['From'] = me
        msg['To'] = you
        # text = "Hi Anurag!\nIt seems Downloadming has been updated recently"
        html = """\
                <html>
                  <head></head>
                  <body>
                    <h2>Hi Anurag!</h2>
                       <p>It seems <a href="https://downloadming.cool/category/bollywood-mp3">Downloadming</a> has been updated recently.</p>
                       <p>The new album added to the list</p>
                       {}{}{}
                  </body>
                </html>
                """.format("<li>", [x for x in updated_album_urls[0]], "</li>")
        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        # msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        # server.login(user='email', password='password')
        server.login(user='an.anuraag@gmail.com', password='3UnTy!3###3')
        server.sendmail(
            me, you, msg.as_string()
        )
        server.quit()
        print("mail sent")
    print(updated_album_urls)
    write_file = open('album_records.txt', 'a')
    write_file.write(f"Date: {datetime.today()}, Top album: {live_album_urls[0][26:]} Album count: {len(live_album_urls)} \n")
    write_file.close()
    new_count = int(len(live_album_urls))
    write_file.close()
