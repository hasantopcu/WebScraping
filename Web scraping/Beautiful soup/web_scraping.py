import bs4 as bs
import urllib.request
import pandas as pd
import requests

domain = 'https://www.hurriyetemlak.com'

current_home = {}
all_homes = []

def start(lb,ub):
    for i in range(lb,ub):
        print('2') 
        sauce = urllib.request.urlopen(domain +'/kiralik-sahibinden?page=' + str(i)).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        list_of_home = soup.find('div' , id='listview')
        links = list_of_home.find_all('a' , class_='overlay-link') 
        for a in links:
            print('5')
            print(a.get('href'))
            
            res =  requests.get(domain + a.get('href'))
            if res.status_code == 200:
                sauce_2 = urllib.request.urlopen(domain + a.get('href')).read()
                soup_2 = bs.BeautifulSoup(sauce_2,'lxml')
                
                current_home.clear()
                
                li_address = soup_2.find('li' , id="realty-adress-line")
                names = li_address.find_all(['a'])
                current_home['il'] = names[0].text.strip()
                current_home['ilce'] = names[1].text.strip()
                current_home['Mahalle'] = names[2].text.strip()

                li_price = soup_2.find('li' , class_="price-line clearfix")
                current_home['Fiyat'] = li_price.text.strip()

                li_ilanNo = soup_2.find('li' , class_='realty-numb')
                ilan_no = li_ilanNo.text.split(':')
                current_home['ilan no'] = ilan_no[1].strip()

                li = soup_2.find('li' , class_="info-line")
                for i in li.find_all(['li']):
                    x = i.find_all(['span'])
                    if len(x) > 0:
                        current_home[x[0].find(text=True).strip()] = x[1].find(text=True).strip()
                all_homes.append(current_home.copy())
            if res.status_code == 404:
                all_homes.append(current_home.copy())    
                print('Acces denied')
                        
    

    tocsv()

def tocsv():
    pd.DataFrame(all_homes).to_csv('home_informations.csv' )
    


if __name__ == "__main__":
    start(1,10)
