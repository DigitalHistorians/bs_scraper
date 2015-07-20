__author__ = 'jerzydem'


def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)


def contains_digits(d):
    # DUPLICATE FUNCTION IN extractor.py
    # TODO - remove duplication
    import re
    _digits = re.compile('\d')
    return bool(_digits.search(d))


def get_csv_headers(results_list):
    # DUPLICATE FUNCTION IN extractor.py
    # TODO - remove duplication
    # prepare list of columns headers for csv file

    headers = []
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
    # DUPLICATE FUNCTION IN extractor.py
    # TODO - remove duplication
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


def clean_place_and_year(str):
    # print(str.replace('k.', 'koło').replace('pow.', 'powiat'))
    return str.replace('k.', 'koło').replace('pow.', 'powiat').replace('n.', 'nad')


def get_first_part(str):
    # TODO refactor names and method
    index = len(str)
    srednik = str.find(';')
    dot = str.find('.')
    coma = str.find(',')
    index = srednik if srednik > 1 and srednik < index else index
    index = dot if dot > 1 and dot < index else index
    index = coma if coma > 1 and coma < index else index

    # print (str.substr(0,index))
    return  str.substr(0,index)


def get_date(str):
    import re

    pattern_date = r'^[AZ]{1}m\. (?P<date>\d{1,2}\.\d{1,2}\.\d{4})'
    pattern_year = r'^[A-Z][a-z][\w\W]+(?P<year>\d{4})[\w\W]+'

    r = re.compile(pattern_date)
    m = r.match(str)
    if not m:
        # if can't find full date - looking for year
        r = re.compile(pattern_year)
        m = r.match(str)

    if m:
        return m.group(1)
    return None

# def get_place(str):
#     # TODO refactor name and method
#     if str.find('ochowany') >= 0:
#         place = str.split('ochowany')[1]
#         print(place[1])


def get_place(str):
    import re
    # TODO get second word if needed

    pattern_place = r'^[AZ]{1}m\. \d{1,2}\.\d{1,2}\.\d{4}\,?\s([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńł]+)'
    pattern_in_place = r'^[A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńł][\w\W]+\d{4}[a-zśćźżąęóńł\s\w]*\sw\s[a-zśćźżąęóńł\s]*([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńł]+)'

    clean_str = clean_place_and_year(str)
    r = re.compile(pattern_place)
    m = r.match(clean_str)
    if not m:
         # if can't find simple place - looking for place after 'w'
         r = re.compile(pattern_in_place)
         m = r.match(str)
         if m:
             str = m.group(1)
             # TODO add if() to correct names


             return str
         else:
             return None
    else:
        return m.group(1)
    return None

#     # TODO - get from str words with first capital letters. Ignore when
#     place = None
#     splited = str.split('w')
#     if len(splited) > 1 and contains_digits(splited[0]):
#         place = get_first_part(splited[1])
#     else:
#         splited = str.split(',')
#         if len(splited) > 1:
#             place = get_first_part(splited[1])
#             if place.split()[0] == 'pochowany' or place.split()[0] == 'Pochowany':
#                 return None
#             else:
#                 return table[1].split('.')[0].strip()


def init_cleaner():
    import sys
    import csv

    EXTRACTED_CSV = "sejm_ustawodawczy/extracted_sejm_ustawodawczy_ii_rp.csv"
    CLEANED_CSV = 'sejm_ustawodawczy/cleaned_sejm_ustawodawczy_ii_rp.csv'


    # INLINE ARGUMENTS
    # use inline arguments if exist
    input_csv = sys.argv[1] if len(sys.argv) > 1 else EXTRACTED_CSV
    output_csv = sys.argv[2] if len(sys.argv) > 2 else CLEANED_CSV

    input_file = open(input_csv)

    # open csv and get rows
    reader = csv.reader(input_file, delimiter=',')

    results_list = []
    headers = []
    for row_num, row in enumerate(reader):
        if row_num == 0:
            headers = row
        else:
            obj = {}
            for coll_num, cell in enumerate(row):
                cell_header = headers[coll_num]
                # print('coll: ', coll_num, 'cell: ', cell, 'row_num: ', row_num, 'row: ', row)
                # print(headers[coll_num])
                if cell_header == 'miejsce-i-rok-smierci':
                    str = clean_place_and_year(cell)
                    obj['data-smierci'] = get_date(str)
                    obj[cell_header] = clean_place_and_year(str)
                    obj['miejsce-smierci'] = get_place(str)
                    # get_grave_place(cell)
                else:
                    # print(stripNonAlphaNum(cell))
                    obj[cell_header] = cell

            results_list.append(obj)

    input_file.close()

#    print(results_list)
    save_to_csv(results_list, output_csv)

init_cleaner()