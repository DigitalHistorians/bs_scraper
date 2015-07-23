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
    # TODO add sort for header
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
    headers.sort()
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


def find_regex_value(patterns_list, string):
    import re
    pattern = patterns_list[0]
    r = re.compile(pattern)
    m = r.match(string)
    if m:
        return m.group(1)
    elif len(patterns_list) <= 1:
        return None
    else:
        return find_regex_value(patterns_list[1:], string)


def replace_abbreviations(string):
    return string.replace(' k.', ' koło').replace(' pow.', ' powiat').replace(' n.', ' nad')


def get_first_part(string):
    # TODO refactor names and method
    index = len(string)
    srednik = string.find(';')
    dot = string.find('.')
    coma = string.find(',')
    index = srednik if srednik > 1 and srednik < index else index
    index = dot if dot > 1 and dot < index else index
    index = coma if coma > 1 and coma < index else index

    # print (str.substr(0,index))
    return  string.substr(0,index)


def find_regex_value(patterns_list, string):
    import re
    pattern = patterns_list[0]
    r = re.compile(pattern)
    m = r.match(string)
    if m:
        return m.group(1)
    elif len(patterns_list) <= 1:
        return None
    else:
        return find_regex_value(patterns_list[1:], string)

def get_date(string):

    pattern_date = r'^[AZ]{1}m\. (?P<date>\d{1,2}\.\d{1,2}\.\d{4})'
    pattern_year = r'^[A-Z][a-z][\w\W]+(?P<year>\d{4})[\w\W]+'

    patterns_list = [pattern_date, pattern_year]
    return find_regex_value(patterns_list, string)


    # r = re.compile(pattern_date)
    # m = r.match(str)
    # if not m:
    #     # if can't find full date - looking for year
    #     r = re.compile(pattern_year)
    #     m = r.match(str)
    #
    # if m:
    #     return m.group(1)
    # return None

# def get_place(str):
#     # TODO refactor name and method
#     if str.find('ochowany') >= 0:
#         place = str.split('ochowany')[1]
#         print(place[1])

def place_nominative(place):
    # TODO make this function - check last chars and replace
    return place


def convert_place(place_str):

    tokens = place_str.split()
    if tokens[0] == 'w':
        pattern = '[a-zśćźżąęóńł\s]*([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńł]+[\w\W]+$)'
        place = find_regex_value([pattern], place_str)
        if place_str.find('obozie') > 0:
            return place
        else:
            return place_nominative(place)
    else:
        return place_str


def get_place(string):
    # TODO get second word if needed - recognize first word of place and get all string to end signs (;,.)

    pattern1_place = r'^[A-Z][a-z][\w\W]+\d{1,2}\.\d{1,2}\.\d{4}\,?\s([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńłA-ZŚĆŹŻÓŃŁ\-\(\)]+)'
    pattern2_place_only_year = r'^[A-Z][a-z][\w\W]+\d{4}\,?\s([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńłA-ZŚĆŹŻÓŃŁ\-\(\)]+)'
    pattern3_place_string_month =r'^[A-Z][a-z][\w\W]+\d{4}\,[a-zśćźżąęóńł\s]*\,\s([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńłA-ZŚĆŹŻÓŃŁ\-\(\)]+)'
    pattern4_in_place = '^[A-Z][a-z][\w\W]+\d{1,2}\.\d{1,2}\.\d{4}[a-zśćźżąęóńł\s]*[\,]?\s(w\s[a-zśćźżąęóńł\s]*[A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńłA-ZŚĆŹŻÓŃŁ\-\(\)]+)'
    pattern5_in_place_only_year = r'^[A-Z][a-z][\w\W]+\d{4}[a-zśćźżąęóńł\s]*[\,]?\s(w\s[a-zśćźżąęóńł\s]*[A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńłA-ZŚĆŹŻÓŃŁ\-\(\)]+)'

    patterns_list = [
        pattern1_place,
        pattern2_place_only_year,
        pattern3_place_string_month,
        pattern4_in_place,
        pattern5_in_place_only_year
    ]

    place_str = find_regex_value(patterns_list, string)
    if place_str:
        return convert_place(place_str)
    return None

    # clean_str = clean_place_and_year(str)
    # r = re.compile(pattern_place)
    # m = r.match(clean_str)
    # if not m:
    #      # if can't find simple place - looking for place after 'w'
    #      r = re.compile(pattern_in_place)
    #      m = r.match(str)
    #      if m:
    #          str = m.group(1)
    #          # TODO add if() to correct names
    #
    #
    #          return str
    #      else:
    #          return None
    # else:
    #     return m.group(1)
    # return None

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

                    cell_str = replace_abbreviations(cell)

                    obj[cell_header] = replace_abbreviations(cell_str)
                    obj['data-smierci'] = get_date(cell_str)
                    obj['miejsce-smierci'] = get_place(cell_str)

                elif cell_header == 'miejsce-i-rok-urodzenia':
                    cell_str = replace_abbreviations(cell)

                    obj[cell_header] = replace_abbreviations(cell_str)
                    obj['data-urodzenia'] = get_date(cell_str)
                    obj['miejsce-urodzenia'] = get_place(cell_str)
                else:
                    # print(stripNonAlphaNum(cell))
                    obj[cell_header] = cell

            results_list.append(obj)

    input_file.close()

#    print(results_list)
    save_to_csv(results_list, output_csv)

init_cleaner()