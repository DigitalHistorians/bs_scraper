__author__ = 'j'


from bs4 import BeautifulSoup
import csv

soup = BeautifulSoup(open("/home/j/Projects/bs_scraper/results2/1_abrahamowicz-dawid-1839-1926.html"))

# print(soup.table.prettify())
table = soup.find('table', cellspacing="2", cellpadding="0")
print(table)

# final_link = soup.p.a
# # final_link.decompose()
#
# f = csv.writer(open("sejm.csv", "w"))
# f.writerow(["Name", "Link"])    # Write column headers as the first line
#
# links = soup.find_all('a')
# for link in links:
#     names = link.contents[0]
#     fullLink = link.get('href')
#
#     f.writerow([names,fullLink])