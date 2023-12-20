from PIL import Image, ImageDraw
from urllib.parse import urlencode
import requests
import io

def download_images(url, yesno): # функция, принимающая на вход два аргумента url(ссылку на изображение), и yesno(будет скачивать с яндекс диска, или нет)

    if yesno == 'yes' or yesno == 'да' or yesno == '1':

        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = url

        final_url = base_url + urlencode(dict(public_key=public_key)) # формируем конечную ссылку для установки фото с яндекс диска
        response = requests.get(final_url)
        download_url = response.json()['href']

        resp = requests.get(download_url, stream = True).raw
        im = Image.open(resp)
        im.save('picture.png', 'png') # сохраняем картинку с названием picture.png

    else:

        resp = requests.get(url, stream = True).raw
        im = Image.open(resp)
        im.save('picture.png', 'png')

def func_watermark(im, watermark): # функция, добавляющая на фото водяной знак

    im.paste(watermark, (0, 0), mask = watermark)
    im.save('picture_out.png', 'png')

try:

    yesno = str(input('Хотите ли вы загрузить изображение с яндекс диска или нет? (yes/no): '))
    url = str(input('Введите ссылку на изображение: '))

    download_images(url, yesno)

    im = Image.open('picture.png')
    watermark = Image.open('watermark.png')

    maxsize = im.size
    watermark = watermark.resize(maxsize) # масштабируем водяной знак относительно изображения

    func_watermark(im, watermark)

except:
    print('Неправильные данные...')