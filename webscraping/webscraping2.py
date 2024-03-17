from bs4 import BeautifulSoup
import requests
import urllib.request
import os 

DATA_DIRECTORY = "scraped_content"
if(DATA_DIRECTORY not in os.listdir()):
    os.mkdir(DATA_DIRECTORY)
url1= 'https://whc.unesco.org/en/list/'
page = requests.get(url1).content
soup = BeautifulSoup(page, 'lxml')
list_sites = soup.find_all('div',class_='list_site')
count=0
number = 0
for list_site in list_sites:
    lis = list_site.find_all('li')
    for li in lis:
        if (li['class'] != ' natural ' ):
            url2 = 'https://whc.unesco.org' + li.a['href']
            name = li.a.text
            #print(name)
            #print(url2)
            nextpage = requests.get(url2).content
            soup2 = BeautifulSoup(nextpage, 'lxml')
            paraspace = soup2.find('main')
            try:
                paragraph = paraspace.find('p').text.strip()
            except AttributeError:
                continue
            locdat = paraspace.find('div',class_='d-flex mb-3')
            #print(location)
            try:
                location = locdat.find('a').text
                latandlongdat = paraspace.find('div',class_='mt-3 small text-muted').text
            except  AttributeError:
                continue
            lines = latandlongdat.splitlines()
            lines = [line.strip() for line in lines]
            latandlongdat= "\n".join(lines).strip()
            last_n_index = latandlongdat.rfind("N")
            latandlong = latandlongdat[last_n_index:]
            #print(latandlong)
            #print(latandlongdat)
            #print(paragraph)
            classw = soup2.find('div',class_='border-top mt-4 pt-4')
            try:
                image = classw.find('img')
                link = image['src']
            except AttributeError:
                continue
            #os.mkdir(name)
            #urllib.request.urlretrieve(link,f'{name}/{name}.jpg')
            #with open(f'{name}/paragraph.txt','a+') as u:
            #    u.write(paragraph)
            #mappage = paraspace.find('ul',class_='nav nav-tabs mb-4')
            #lias = mappage.find_all('li')
            #maplink ='https://whc.unesco.org' + lias[1].a['href']
            #print(maplink)
            #maptext = requests.get(maplink).content
            #soup3 = BeautifulSoup(maptext,'lxml')
            #maptable = soup3.find('table',class_='table table-striped table-hover table-sm')
            try:
                #tds = maptable.find_all('td')
                #coordinate = tds[3].text.strip()
                #print(name)
                os.mkdir(f'scraped_content/{name}')
                with open(f'scraped_content/{name}/location.txt','a+') as k:
                    k.write(location)
                with open(f'scraped_content/{name}/coordinate.txt','a+') as j:
                    j.write(latandlong)
                urllib.request.urlretrieve(link,f'scraped_content/{name}/{name}.jpg')
                with open(f'scraped_content/{name}/paragraph.txt','a+') as u:
                    u.write(paragraph)
                count = count+1
                print(count)
            except (AttributeError,FileExistsError,FileNotFoundError):
                continue
            #coordinate = tds[3].text.strip()
            #print(coordinate)
            
    number = number+1
    if number == 20:
        print('Done!')
        break