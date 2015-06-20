__author__ = 'j'
import os
import csv
folder_path = "/home/j/Projects/bs_scraper/results2"

def get_page_data(page_source):
    from slugify import slugify
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(open(page_source))
    table_list = soup.body.find_all('table', recursive=False)
    if len(table_list) is not 5:
        print("WARNING: unexpected structure: body", len(table_list))
    else:
        main_table = table_list[4]
        table = main_table.find('table', width="100%", border="0", cellspacing="2", cellpadding="0")
        if table is None:
            print("SINGLE TABLES LEVEL")
            table = main_table
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

def define_headers(results_list):
    headers = []
    result_index = 0
    for result_line in results_list:
        label_index = 0
        if result_line is None:
            # TODO define and resolve this problem
            print("WARNING: Result line: ", result_index, "label_index: ", label_index)
            print("Result before", results_list[result_index-1])
            print("Current result: ", results_list[result_index])
        else:
            for label in result_line:
                if not any(label in s for s in headers):
                    headers.append(label)
                label_index += 1
        result_index += 1
    return headers

def prepare_csv(results_list):
    import csv
    headers = define_headers(results_list)
    print(headers)
    f = csv.writer(open("sejm_ustawodawczy_ii_rp.csv", "w"))
    f.writerow(headers)    # Write column headers as the first line
    result_index = 0
    for result_line in results_list:
        label_index = 0
        if result_line is None:
            # TODO define and resolve this problem
            print("WARNING: Result line: ", result_index, "label_index: ", label_index)
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


results_list = []
index = 0

for filename in os.listdir(folder_path):
    index += 1
    # print(index, ': ', folder_path+'/'+filename)
    results_list.append(get_page_data(folder_path+'/'+filename))
# print(results_list)
prepare_csv(results_list)


