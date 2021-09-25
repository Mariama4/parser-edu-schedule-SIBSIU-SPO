from urllib.request import urlopen
from lxml import etree
import requests as request
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path



local = 'https://www.sibsiu.ru/raspisanie/'                 # директория сайта с расписанием

response = urlopen(local)                                   # получение сайта через urlib (можно и через request)

htmlParser = etree.HTMLParser()                             # парс данных
tree = etree.parse(response, htmlParser)                    #

el = tree.xpath('//*[@id="inst10"]/ul/ul[6]/ul[6]/li/a')    # поиск в структуре нужного расписания через xpath

mainFileLink = str(el[0].attrib)[10:-22]                    # удаление лишних данных в строках
local = local[0:-12]                                        #
mainFileLink = mainFileLink.replace('\\\\', '/')            #

mainGoal = local + mainFileLink                             # получение полной ссылки с .pdf файлом расписания

res = request.get(mainGoal)                                 # получение сайта через request (можно и через urlib)

res.encoding = 'utf-8'                                      # установка кодировка файла

lastModified = res.headers['Last-Modified']                 # получение нужных данных из хедера (получаем дату последнего изменения файла)
                                                            # можно использовать для отслеживания актуального расписания

with open('main.pdf', 'wb') as f:                           # сохранения .pdf
    f.write(res.content)                                    #

popplerPath = "poppler-21.09.0\\Library\\bin"               #
images = convert_from_path('main.pdf',                      # конвертирование из .pdf в .png
                           300,                             # качество 300 dpi
                           poppler_path=popplerPath)        #

outputPath = 'raspisanie.png'                               # путь для сохранения .png
images[0].save(outputPath)                                  # сохранение первого листа .pdf (в моем случае) в .png в указанный путь