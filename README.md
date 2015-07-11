# BS Scraper
BS Scraper is script to download and extract to csv biographic data from ["Biblioteka Sejmowa"](installation instructions]https://bs.sejm.gov.pl/F?func=scan&scan_code=KS2&x=0&y=0&scan_start=1919)

## Dependencies
BS Scraper need following Python 3 libraries:
 - urllib
 - slugify
 - time
 - csv
 - BeautifulSoup

## Download pages (`get_files.py`)

To download html files run get_files.py

```
python3 get_files.py start_num input_csv
```

`input_csv` - optional: input_csv with names (format: NUMBER, NAME)
`start_num` - optional: start row in input_csv


## Extract data

To extract data run extractor.py