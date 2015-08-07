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
    slug_name = slugify(name)

    # detect if server is down. When server is down, result pages are very small
    if size < 1000:
        # BS Server down
        print('SERVER OFF {:>4} {} SIZE: {}'.format(index, url, size))
        time.sleep(4)
        get_page(name, index, destination)
    else:
        # Page size is enough. Save page
        print(index, ' Name: ', name, ' ', url)
        file_name = destination + 'html/' + str(index) + '_' + slug_name + '.html'
        f = open(file_name, 'wb')
        f.write(web_content)
        f.close
        get_image_url(file_name, slug_name, destination + 'img/')

    # 5 seconds timeout to limit server pauses
    time.sleep(3)


def download_image(url, name, destination):
    import urllib.request
    import urllib.parse
    response = urllib.request.urlopen(url)
    web_content = response.read()
    f = open(destination + name + '.jpg', 'wb')
    f.write(web_content)
    f.close


def get_image_url(file_path, name, destination):
    from bs4 import BeautifulSoup

    server_url = 'https://bs.sejm.gov.pl/'
    # pattern = r'^javascript\:open\_window\(\"([\w\W]*)\"\)\;$'

    # print("GET IMAGE: ", file_path)
    soup = BeautifulSoup(open(file_path))
    image_cell = soup.body.find('td', align="center", valign="top", style="padding-top: 8px;");
    if image_cell:
        href = image_cell.a['href']
        full_src = server_url + image_cell.a.img['src']

        # get url of big
        # r = re.compile(pattern)
        # m = r.match(href)
        # print("Small: ", full_src)
        download_image(full_src, name, destination)
        # if m:
        #     full_href = server_url + '/F/' + m.group(1)
        #     print('Full href: ', full_href)
        #     download_image(full_href, 'big_' + name)


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
    destination_folder = sys.argv[3] + '/' if len(sys.argv) > 3 else DESTINATION_FOLDER

    csv_get_all_pages(input_csv, start_row, destination_folder)

init_getter()
