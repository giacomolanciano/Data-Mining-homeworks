import os.path
from os import listdir
import unicodecsv as csv
from bs4 import BeautifulSoup
import time
import re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes')
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes.tsv')
HEADER = ['title', 'author', 'prep_time', 'cook_time', 'serves',
               'dietary_info', 'description', 'ingredients', 'method', 'url_id']

if __name__ == "__main__":
    start_time = time.time()

    # parse recipes and put data in a single .tsv file
    with open(DEST, 'wb') as out:
        tsv_writer = csv.writer(out, delimiter='\t', encoding='utf-8')
        tsv_writer.writerow(HEADER)

        for f in listdir(SRC):
            print f
            row = []
            fid = open(os.path.join(SRC, f), 'r')
            recipeSoup = BeautifulSoup(fid, 'html.parser')

            try: row.append(recipeSoup.find('h1', class_='content-title__text').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            try: row.append(recipeSoup.find('a', class_='chef__link', itemprop='author').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            try: row.append(recipeSoup.find('p', class_='recipe-metadata__prep-time').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            try: row.append(recipeSoup.find('p', class_='recipe-metadata__cook-time').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            try: row.append(recipeSoup.find('p', class_='recipe-metadata__serving').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            try: row.append(recipeSoup.find('p', class_='recipe-metadata__dietary-vegetarian-text').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            try: row.append(recipeSoup.find('p', class_='recipe-description__text').text.strip().replace('\n', ' '))
            except AttributeError: row.append('')

            ingredients = []
            for i in recipeSoup.find_all('li', class_='recipe-ingredients__list-item'):
                ingredients.append(i.text.strip().replace('\n', ' '))
            row.append(" | ".join(ingredients))

            method = []
            for m in recipeSoup.find_all('p', class_='recipe-method__list-item-text'):
                method.append(m.text.strip().replace('\n', ' '))
            row.append(" | ".join(method))

            row.append(re.sub(r'\.html', '', f))

            tsv_writer.writerow(row)
            fid.close()

    print("\n--- %s seconds ---" % (time.time() - start_time))