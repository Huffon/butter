from bs4 import BeautifulSoup as bs
import random
import urllib
import requests

def get_img(source):
    htmlreq = "https://www.google.com/search?q={source}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj_hpGs8OzcAhWOfd4KHSILBIYQ_AUICigB&biw=1536&bih=759&dpr=1.25"
    htmlreq = htmlreq.format(source=urllib.parse.quote(source))

    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(htmlreq, headers=headers)

    soup = bs(response.text, 'html.parser')
    imgs = soup.find_all('img')

    index = random.randint(1, len(imgs)-1)
    src = imgs[index].get('src')

    return src
