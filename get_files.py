__author__ = 'jerzydem'


def get_page(name, index):

    import urllib.request
    import urllib.parse
    import sys
    import time
    from slugify import slugify

    names_table = name.replace('?', ' ').replace('-', ' ').split()
    name_query = '';
    for token in names_table:
        if token != "ksiądz":
            name_query += urllib.parse.quote(token)
            name_query += "+"


    encoded_url = "https://bs.sejm.gov.pl/F/?func=find-b&request=" + name_query + \
                  "&find_code=WRD&adjacent=N&x=27&y=6&local_base=ars10"

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
        f = open('results2/' + str(index) + "_" + slugify(name) + ".html", 'wb')
        f.write(web_content)
        f.close



def csv_get_all_pages(csv_file):
    import time
    import csv

    ifile  = open(csv_file)
    reader = csv.reader(ifile, delimiter=',')

    rownum = 0
    for row in reader:
        if rownum > 0:
            name = row[1]
            get_page(name, rownum)
        rownum += 1

    ifile.close()

csv_get_all_pages("files/sejm_ustawodawczy.csv")