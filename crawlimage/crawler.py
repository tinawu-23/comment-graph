# crawl fake images from http://hoaxes.org

import requests
from bs4 import BeautifulSoup
import urllib.request

timeperiods = ['before_1900', '1900_1919',
               '1920_1939', '1940_1959', '1960_1979', '1980_1999', '2000_2004', '2005_Present']

pages = ['/', '/P18', '/P36']


baseurl = 'http://hoaxes.org/photo_database/years/category/'

for timeperiod in timeperiods:
    for page in pages:
        url = baseurl + timeperiod + page
        try:
            source = requests.get(url)
        except:
            continue
            
        data = source.text
        soup = BeautifulSoup(data, 'html.parser')
        imgtags = soup.find_all('img')
        imageurls = [img['src'] for img in imgtags]
        for imgurl in imageurls:
            if 'png' in imgurl:
                continue
            #print(imgurl)
            imgname = imgurl.split('/')[-1]
            print(imgname)
            imgname = 'images/' + imgname
            print(imgname)
            urllib.request.urlretrieve(imgurl, imgname)
    
