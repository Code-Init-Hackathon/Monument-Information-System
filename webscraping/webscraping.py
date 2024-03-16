from bs4 import BeautifulSoup
import requests
import urllib.request
import os 
#url = 'https://en.wikipedia.org/wiki/Eiffel_Tower'
def get_data():
    html_text = requests.get(url).content
    soup = BeautifulSoup(html_text, 'lxml')
    name = soup.find('span',class_='mw-page-title-main').string
    print(name)
    table=soup.find('td',class_='infobox-image')
    image = table.find('img')
    link = 'http:' + image['src']
    os.mkdir(name)
    urllib.request.urlretrieve(link,f'{name}/{name}.jpg')
    print('image added')
    latitude = soup.find('span',class_='latitude').text
    longitude = soup.find('span',class_='longitude').text
    with open(f'{name}/{name}.txt','w') as f:
        f.write(f'{latitude}\\n')
        f.write(f'{longitude}')
        print('location')

if __name__ == '__main__':
    urls=('https://en.wikipedia.org/wiki/Angkor_Wat','https://en.wikipedia.org/wiki/Caral','https://en.wikipedia.org/wiki/Colosseum','https://en.wikipedia.org/wiki/Charminar','https://en.wikipedia.org/wiki/Golden_Gate_Bridge','https://en.wikipedia.org/wiki/Grand_Central_Terminal','https://en.wikipedia.org/wiki/Great_Pyramid_of_Giza','https://en.wikipedia.org/wiki/Kinkaku-ji','https://en.wikipedia.org/wiki/Kremlin','https://en.wikipedia.org/wiki/Leaning_Tower_of_Pisa','https://en.wikipedia.org/wiki/Madrid_Atocha_railway_station','https://en.wikipedia.org/wiki/Masjid_al-Haram','https://en.wikipedia.org/wiki/Notre-Dame_de_Paris','https://en.wikipedia.org/wiki/Palace_of_Versailles','https://en.wikipedia.org/wiki/Palace_of_Westminster','https://en.wikipedia.org/wiki/Pantheon,_Rome','https://en.wikipedia.org/wiki/Pergamon','https://en.wikipedia.org/wiki/Persepolis','https://en.wikipedia.org/wiki/Qutb_Minar','https://en.wikipedia.org/wiki/Red_Square','https://en.wikipedia.org/wiki/Sanchi','https://en.wikipedia.org/wiki/Shwedagon_Pagoda','https://en.wikipedia.org/wiki/Sydney_Harbour_Bridge','https://en.wikipedia.org/wiki/Sydney_Opera_House','https://en.wikipedia.org/wiki/Taj_Mahal','https://en.wikipedia.org/wiki/United_States_Capitol','https://en.wikipedia.org/wiki/White_House','https://en.wikipedia.org/wiki/Ziggurat_of_Ur','https://simple.wikipedia.org/wiki/Alhambra','https://simple.wikipedia.org/wiki/Borobudur','https://simple.wikipedia.org/wiki/Eiffel_Tower','https://simple.wikipedia.org/wiki/Forbidden_City','https://simple.wikipedia.org/wiki/Kiyomizu-dera','https://simple.wikipedia.org/wiki/Machu_Picchu','https://simple.wikipedia.org/wiki/Petra')
    for url in urls:
        print(url)
        get_data()