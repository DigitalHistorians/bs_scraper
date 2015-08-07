__author__ = 'jerzydem'


EXTRA_COLUMNS_HEADERS = [
    'osoba',
    'daty-zycia',
    'rok-urodzenia',
    'miejsce-i-rok-urodzenia',
    'rok-smierci',
    'miejsce-i-rok-smierci',
    'baza'
]


def contains_digits(d):
    import re
    _digits = re.compile('\d')
    return bool(_digits.search(d))


def containsAny(str, set):
    # Check whether 'str' contains ANY of the chars in 'set
    return 1 in [c in str for c in set]


def get_year(soap):
    from bs4 import NavigableString, Tag

    fields = soap.find_all('span')

    for field in fields:
        text = field.string.strip()

        if contains_digits(text):
            return text.strip('.')

    return None


def extract_data_from_table(source_table):
    from slugify import slugify
    from bs4 import NavigableString, Tag

    # 4) get all rows
    rows_list = source_table.find_all('tr')
    results = {}
    content_id = None

    for row in rows_list:
        cells = row.find_all('td', recursive=False)

        if len(cells) < 1:
            print("EXTRACTOR ERROR")
            return
        label = slugify(cells[0].string)

        if label == 'biografia':
            # get extra columns from 'biografia'
            text = cells[1].get_text().strip()
            if text[-1] != '.':
                text += '.'
            content_id = label
            results[content_id] = text
            results['miejsce-i-rok-urodzenia'] = text

            birth_year = get_year(cells[1])

            if birth_year:
                results['rok-urodzenia'] = birth_year

        elif label == 'nazwisko-i-imię':
            # get extra columns from 'nazwisko i imię'
            content_id = label
            results[content_id] = cells[1].get_text().strip()

            name_fields = cells[1].a.contents
            name = ''
            date = ''

            for index, field in enumerate(name_fields):

                if isinstance(field, Tag):
                    text = field.get_text().strip()

                    if text == 'ok':
                        date += text

                    elif contains_digits(text):
                        date += ' ' + text

                    else:
                        name += ' ' + text

                elif isinstance(field, NavigableString):
                    text = field.string.strip()

                    if contains_digits(text) or containsAny(text, '()?'):
                        date += ' ' + text
                    else:
                        name += ' ' + text

            results['osoba'] = name.strip()
            results['daty-zycia'] = date.strip()

        elif len(label) > 0:
            # if label is not empty (row has title) - create new position in results
            content_id = label
            results[content_id] = cells[1].get_text().strip()

        else:
            # if row has not title

            if content_id == 'biografia':
                # it's second row of 'biografia'
                text = cells[1].get_text().strip()
                if text[-1] != '.':
                    text += '.'

                results[content_id] += text
                results['miejsce-i-rok-smierci'] = text
                death_year = get_year(cells[1])

                if death_year:
                    results['rok-smierci'] = death_year

            elif content_id == 'wyświetl' or\
                            content_id == 'nazwisko-i-imię' or\
                            content_id == 'trop-zobacz' or\
                            content_id == 'marszałek-rp-':
                # it's first row of baza's lists
                content_id = 'baza'
                results[content_id] = cells[1].get_text().strip()

            else:
                # add value to last position in results
                results[content_id] += ' | ' + cells[1].get_text().strip().strip('-')

    return results


def get_image(soup):
    # find in soup url of photo
    # TODO - remove - hash change in database url
    result = None
    url = 'https://bs.sejm.gov.pl'
    image_table = soup.find('table', border='0', cellpadding='10', cellspacing='0')

    if image_table:
        result = url + image_table.find('img').get('src')

    return result


def get_page_data(page_source):
    # init soup and check proper structure of html

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(open(page_source))
    # find in 'body' element 5 'table' children
    table_list = soup.body.find_all('table', recursive=False)

    # detect wrong html file
    if len(table_list) is not 5:
        print('WARNING: unexpected structure in ', page_source, ': body should have 5 table children - has ', len(table_list))

    else:
        # 1) get 4'th table from table_list
        main_table = table_list[4]

        # 2) find source_table by with, border, cellspacing and cellpadding attributes
        source_table = main_table.find('table', width='100%', border='0', cellspacing='2', cellpadding='0')

        # 3) if can't find source_table: main_table is suorce_table
        if source_table is None:
            # print('Source table is body child')
            source_table = main_table

    # 4) init extraction from source_table
    results = extract_data_from_table(source_table)

    # 5) find image src and add to results
    image_src = get_image(soup)

    if image_src:
        results['zdjecie'] = image_src

    return results


def get_csv_headers(results_list):
    # prepare list of columns headers for csv file

    headers = EXTRA_COLUMNS_HEADERS
    result_index = 0

    for result_line in results_list:
        label_index = 0

        if result_line is None:
            print('WARNING: result_line is None')

        else:

            for label in result_line:

                if not any(label in s for s in headers):
                    headers.append(label)
                label_index += 1

        result_index += 1

    return headers


def save_to_csv(results_list, name):
    # prepare csv with headers and all results rows

    import csv

    headers = get_csv_headers(results_list)
    print(headers)

    f = csv.writer(open(name, 'w'))
    f.writerow(headers)    # Write column headers as the first line
    result_index = 0

    for result_line in results_list:
        label_index = 0

        if result_line is None:
            print('WARNING: Result line is None. result index: ', result_index, 'label_index: ', label_index)

        else:
            csv_line = []

            for name in headers:
                try:
                    csv_line.append(result_line[name])
                except KeyError:
                    csv_line.append('')
                    continue
            f.writerow(csv_line)

        result_index += 1


def init_extractor():
    # start extractor

    import os
    import sys

    HTML_FOLDER = 'sejm_ustawodawczy/html/'
    OUTPUT_CSV = 'sejm_ustawodawczy/extracted_sejm_ustawodawczy_ii_rp.csv'

    results_list = []
    index = 0

    # INLINE ARGUMENTS
    # use inline arguments if exist
    html_files_folder = sys.argv[1] if len(sys.argv) > 1 else HTML_FOLDER
    output_csv_file = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_CSV

    # iterate in HTML_FOLDER and extract data from every file
    for filename in os.listdir(html_files_folder):
        index += 1
        # print(index, ': ', HTML_FOLDER+'/'+filename)
        extracted_data = get_page_data(html_files_folder+'/'+filename)

        if extracted_data is None:
            print(index, ': ', html_files_folder+'/'+filename)
            print('WARNING: extracted data is NONE!!! - ignore file')

        else:
            results_list.append(extracted_data)

    save_to_csv(results_list, output_csv_file)

init_extractor()