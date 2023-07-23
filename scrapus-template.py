#imports

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

#website to be scraped
baseurl = 'https://www.tagesschau.de/'
headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36'
}

#access website
r = requests.get(baseurl)
soup = BeautifulSoup(r.text, 'html.parser')

#access the articles contents
articlelist = soup.body.find_all('div', attrs={'class', 'teaser'})

#Find all article links on the main page

articlelinks = []

for item in articlelist:
    articlelist = item.a.attrs['href']
    articlelinks.append(articlelist)

#Remove all links that do not start with tagesschau

filter = "https://www.tagesschau.de/"

filtered = [x for x in articlelinks if x.startswith(filter)]


#testlink = 'https://www.tagesschau.de/inland/corona-bund-103.html'

information_list = []
for link in filtered:

    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    article = soup.find('article', attrs={'container'})

    title = soup.find('span', class_='meldungskopf__headline--text')
    subtitle = soup.find('span', class_='meldungskopf__topline')
    date = soup.find('p', class_='meldungskopf__datetime')

    try:
        author = soup.find('span', class_='autorenzeile__autor').text.strip()
    except:
        author = ' '



#try finding  a way to have all paragraphs !DONE!

    #for item in paragraph:
    #    paragraphs = item.text.encode('utf-8').strip()
    #    paragraphs_final.append(paragraphs)

    keywords_final = []
    key = soup.find_all(class_='taglist__element')

    for item in key:
        keys = item.text.encode('utf-8').strip()
        keywords_final.append(keys)

#try finding  a way to have all paragraphs !DONE!
    paragraphs_final = []
    paragraph = soup.find_all(class_='textabsatz')

    for item in paragraph:
        paragraphs = item.text.encode('utf-8').strip()
        paragraphs_final.append(paragraphs)

    information = {
        'title': title,
        'subtitle': subtitle,
        'date': date,
        'author': author,
        'keywords': keywords_final,
        'paragraphs': paragraphs_final,
    }

    information_list.append(information)

df = pd.DataFrame(information_list)


#names Times

current_date = datetime.datetime.now()
filename =  str(current_date.year) + '-' + str(current_date.month) + '-' + str(current_date.day) + '-' + str(current_date.hour) + ':' + str(current_date.minute)
df.to_csv(str(filename + '.csv'))

print("done!")
