import random
import smtplib
import requests
from bs4 import BeautifulSoup as Soup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    # scrape letest album list
    url = "https://downloadming.cool/category/bollywood-mp3"
    resp = get_response(url)
    my_soup = Soup(resp.text, 'html.parser')
    album_url_list = []
    for li in my_soup.find("section", {'class': 'primary'}).find_all('li'):
        anchor = li.find('a', href=True)['href']
        album_url_list.append(anchor)
    # check last album count
    read_file = open('album_count.txt', 'r')
    lines = read_file.readlines()[-1:]
    old_count = int(lines[0][-6:])
    read_file.close()
    # check live album count
    write_file = open('album_count.txt', 'a')
    write_file.write(f"Date: {datetime.today()}, Top album: {album_url_list[0][26:]} Album count: {len(album_url_list)} \n")
    write_file.close()
    new_count = int(len(album_url_list)) + 1
    write_file.close()
    # if the album has been updated notify using mail
    if old_count == new_count:
        print("Not Changed")
    else:  # If something has changed
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
            <h2>Hi Anurag!</h2><br>
               <p>It seems <a href="https://downloadming.cool/category/bollywood-mp3">Downloadming</a> has been updated recently.</p>
               <p>The new album added to the list</p>
               <li>{}</li>
          </body>
        </html>
        """.format(album_url_list[0][26:])
        # part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        # msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        server.login(user='email', password='password')
        server.sendmail(
            me, you, msg.as_string()
        )
        server.quit()
