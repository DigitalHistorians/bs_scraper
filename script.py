__author__ = 'j'

def get_page(url, index):

    import urllib.request
    response = urllib.request.urlopen(url)
    web_content = response.read()

    f = open('results/posel' + str(index) + ".html", 'wb')
    f.write(web_content)
    f.close


line_number = 0
with open('files/urls_list_sejm_ustawodawczy.txt', encoding='utf-8') as urls_file:
    for single_url_line in urls_file:
        line_number += 1
        print('{:>4} {}'.format(line_number, single_url_line.rstrip()))
        get_page(single_url_line, line_number)


