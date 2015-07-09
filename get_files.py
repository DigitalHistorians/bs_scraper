__author__ = 'jerzydem'
import sys

def get_page(name, index):

    import urllib.request
    import urllib.parse
    import sys
    import time
    from slugify import slugify


    names_table = name.replace('?', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ').split()

    name_query = ''
    for token in names_table:
        if token != "ksiądz":
            name_query += urllib.parse.quote(token)
            name_query += "+"


    encoded_url = "https://bs.sejm.gov.pl/F/?func=find-b&request=" + name_query + \
                  "&find_code=WPN&adjacent=N&x=27&y=6&local_base=ars10"

    response = urllib.request.urlopen(encoded_url)
    web_content = response.read()
    size = sys.getsizeof(web_content)
    time.sleep(5)

    if size < 1000:
        print('SERVER OFF {:>4} {} SIZE: {}'.format(index, encoded_url, size))
        time.sleep(5)
        get_page(name, index)
    else:
        print(index, " Name: ", name, " ", encoded_url)
        f = open('results3/' + str(index) + "_" + slugify(name) + ".html", 'wb')
        f.write(web_content)
        f.close



def csv_get_all_pages(csv_file, start_line):
    import csv

    input_file = open(csv_file)
    # open csv and get rows
    reader = csv.reader(input_file, delimiter=',')

    rows_num = 0
    for row in reader:
        # ignore row if its lower then start_line
        if rows_num > start_line-1:
            name = row[1]
            get_page(name, rows_num)
        rows_num += 1

    input_file.close()


# INITIALIZATION

# CONSTANT VALUES
DEPUTIES_CSV = "files/sejm_ustawodawczy.csv"
START_LINE = 209


# USE INIT INLINE ARGUMENTS
# TODO add short form of "if"
# TODO - test it
if len(sys.argv) > 1:
    start_row = sys.argv[1]
    if len(sys.argv) > 2:
        input_csv = sys.argv[2]
    else:
        input_csv = DEPUTIES_CSV
else:
    start_row = START_LINE



csv_get_all_pages(input_csv, start_row)