import requests
import cyrtranslit
import pandas as pd
from bs4 import BeautifulSoup
from textgenrnn import textgenrnn


url = 'http://txtmusic.ru/index.php?s=%CA%E8%ED%EE'


def get_page(url):
    page = requests.get(url)
    return page.text

def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.findAll('li')
    links = []

    for li in lis:
        a = li.find('a').get('href')
        links.append('http://txtmusic.ru/' + a)
    return links

def get_all_stuff(all_links):

    text_file = open("songs.txt", "w")
    for link in all_links:
        page = get_page(link)
        soup = BeautifulSoup(page, "lxml")
        article = soup.findAll('article')
        text = str(article).split('\n')[8]
        text = text.split('<br/>')
        text = [t for t in text if t != '']

        text = ' '.join(text)
        text = text.replace('\r', ' ')
        text_file.write(text + '\n')
    text_file.close()

def translite(file_in, file_out, ru=''):
    text_file = open(file_out, "w")

    with open(file_in) as f:
        if ru:
            for line in f:
                new_line = cyrtranslit.to_latin(line, 'ru')
                text_file.write(new_line)
        else:
            for line in f:
                new_line = cyrtranslit.to_cyrillic(line)
                text_file.write(new_line)
    text_file.close()

def textgen():
    textgen = textgenrnn()
    textgen.train_from_file('translit.txt', num_epochs=3)

def finish():
    textgen_2 = textgenrnn('textgenrnn_weights.hdf5')
    textgen_2.generate(3, temperature=1.0)
    textgen_2.generate_to_file('lyrics.txt')

def main():
    all_links = get_links(get_page(url))
    get_all_stuff(all_links)
    # translite('songs.txt', 'translit.txt', 'ru')
    textgen()
    finish()
    # translite('lyrics.txt', 'final.txt')







if __name__ == '__main__':
    main()
