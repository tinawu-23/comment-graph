# crawl fake images from http://hoaxes.org
import io
import requests
from bs4 import BeautifulSoup
import urllib.request

timeperiods = ['before_1900', '1900_1919',
               '1920_1939', '1940_1959', '1960_1979', '1980_1999', '2000_2004', '2005_Present']

pages = ['/', '/P18', '/P36']


baseurl = 'http://hoaxes.org/photo_database/years/category/'

f = open("imageTitle.txt", "w")
f.write('FileName\tTitle\n')
ff = open("imageURL.txt", "w")

for timeperiod in timeperiods:
    for page in pages:
        url = baseurl + timeperiod + page
        try:
            source = requests.get(url)
        except:
            continue

        data = source.text
        soup = BeautifulSoup(data, 'lxml')
        imgtags = soup.find_all('img')
        titles = [str(b.text.encode("utf-8"))[1:].replace("'", "").replace("\\xe2\\x80\\x99", "").replace("\\xe2\\x80\\x98", "").replace("\\xe2\\x80\\x9d", "").replace("\\xe2\\x80\\x9c","") for b in soup.find_all('b')
                  if "\\xc2\\xa0\\xc2\\xa0" not in str(b.text.encode("utf-8"))]
        print(titles)

        i = 0
        for img in imgtags:
            try:
                width = img['width']
            except:
                continue

            if width == "100%":
                imgurl = img['src']
                imgname = imgurl.split('/')[-1]
                f.write("{}\t{}\n".format(imgname,titles[i]))
                imgname = 'images/' + imgname
                # print(imgname)
                urllib.request.urlretrieve(imgurl, imgname)
                ff.write(imgurl+'\n')
                i += 1
f.close()
ff.close()