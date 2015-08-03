__author__ = 'jerzydem'

# TODO
# def  get_image


def prepare_page_url(name):
    import urllib
    refine_name = name.replace('?', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ');
    # add name values to table
    names_table = refine_name.split()

    # prepare url query
    name_query = ''
    for token in names_table:
        # ignore token 'ksiądz'
        if token != 'ksiądz':
            name_query += urllib.parse.quote(token)
            name_query += '+'


    encoded_url = 'https://bs.sejm.gov.pl/F/?func=find-b&request=' + name_query + \
                  '&find_code=WPN&adjacent=N&x=27&y=6&local_base=ars10'
    return encoded_url

def get_page(name, index, destination):
    # init page url preparation and save html in destination folder

    import urllib.request
    import urllib.parse
    import sys
    import time
    from slugify import slugify

    url = prepare_page_url(name)

    response = urllib.request.urlopen(url)
    web_content = response.read()
    size = sys.getsizeof(web_content)

    # 5 seconds timeout to limit server pauses
    time.sleep(5)

    # detect if server is down. When server is down, result pages are very small
    if size < 1000:
        # BS Server down
        print('SERVER OFF {:>4} {} SIZE: {}'.format(index, url, size))
        time.sleep(5)
        get_page(name, index, destination)
    else:
        # Page size is enough. Save page
        print(index, ' Name: ', name, ' ', url)
        f = open(destination + str(index) + '_' + slugify(name) + '.html', 'wb')
        f.write(web_content)
        f.close

#def get_image(web_content):
    # TODO finish it


def csv_get_all_pages(csv_file, start_line, destination):
    # get names of members of Sejm from csv file and init single page getter
    import csv

    input_file = open(csv_file)
    # open csv and get rows
    reader = csv.reader(input_file, delimiter=',')

    rows_num = 0
    for row in reader:
        # ignore row if its number is lower then start_line (to start from specific number)
        if rows_num > start_line-1:
            name = row[1]
            get_page(name, rows_num, destination)
        rows_num += 1

    input_file.close()


def init_getter():
    # set init values and start getter
    import sys

    # CONSTANT VALUES
    INPUT_CSV = ''
    START_LINE = 1
    DESTINATION_FOLDER = 'sejm_ii/html/'


    # INLINE ARGUMENTS
    # use inline arguments if exist
    input_csv = sys.argv[1] if len(sys.argv) > 1 else INPUT_CSV
    start_row = int(sys.argv[2]) if len(sys.argv) > 2 else START_LINE
    destination_folder = sys.argv[3] if len(sys.argv) > 3 else DESTINATION_FOLDER

    csv_get_all_pages(input_csv, start_row, destination_folder)

init_getter()
