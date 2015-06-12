__author__ = 'j'
import os
import csv
folder_path = "/home/j/Projects/bs_scraper/results2"

def get_page_data(page_source):
    from slugify import slugify
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(open(page_source))
    table = soup.find('table', cellspacing="2", cellpadding="0")

    rows_list = table.find_all('tr')
    results = {}
    content_id = None
    for row in rows_list:
        cells = row.find_all('td')
        label = slugify(cells[0].string)
        value = cells[1].string
        # print(label, ": ", value)
        if value is not None:
            if len(label) > 0:
                content_id = label
                results[content_id] = value
            else:
                results[content_id] += value

    return results


# TODO test opening files from folder. Base on
#  http://stackoverflow.com/questions/18262293/python-open-every-file-in-a-folder
for filename in os.listdir(folder_path):
    results_list = []
    results_list.append(get_page_data(folder_path+ '/' + filename))




