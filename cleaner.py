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
    # TODO change for regex
    return string\
        .replace(' k.', ' koło')\
        .replace('(b.', '(byłe')\
        .replace(' pow.', ' powiat')\
        .replace('(pow.', '(powiat')\
        .replace(' woj.', ' województwo')\
        .replace('(woj.', '(województwo')\
        .replace(' n.', ' nad')\
        .replace(' obw.', ' obwód')\
        .replace('(obw.', '(obwód')\
        .replace(' gub.', ' gubernia')\
        .replace('(gub.', '(gubernia')\
        .replace(' Maz.', ' Mazowiecki.')\
        .replace(' Wlkp.', ' Wielkopolski.')\
        .replace(' Lub.', ' Lubelski.')\
        .replace('W. Bryta', 'Wielka Bryta')



def get_first_part(string):
    # TODO refactor names and method
    index = len(string)
    srednik = string.find(';')
    dot = string.find('.')
    coma = string.find(',')
    index = srednik if srednik > 1 and srednik < index else index
    index = dot if dot > 1 and dot < index else index
    index = coma if coma > 1 and coma < index else index

    return string.substr(0,index)


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

    pattern_date = r'^[A-Z][a-z][\w\W]+\s(?P<date>\d{1,2}\.\d{1,2}\.\d{4})'
    pattern_year = r'^[A-Z][a-z][\w\W]+\s(?P<year>\d{4})[\w\W]+'

    patterns_list = [pattern_date, pattern_year]
    date = find_regex_value(patterns_list, string)
    return date


def nominative_from_locative(place):

    # TODO use Morfologic to get nominative
    if place is None:
        # print(place)
        return place
    else:
        place += ' '

    nominative_place = place\
        .replace(', ', ' ')\
        .replace('Biesiekierzu-', 'Biesiekierz-')\
        .replace('Gródku ', 'Gródek ')\
        .replace('łce ', 'łka ')\
        .replace('wce ', 'wka ')\
        .replace('pocie ', 'pot ')\
        .replace('ocie ', 'oto ')\
        .replace('amie ', 'am ')\
        .replace('Rzymie ', 'Rzym ')\
        .replace('mie ', 'ma ')\
        .replace('anie ', 'an ')\
        .replace('enie ', 'ena ')\
        .replace('gnie ', 'gno ')\
        .replace('inie ', 'in ')\
        .replace('lnie ', 'lno ')\
        .replace('onie ', 'ona ')\
        .replace('śnie ', 'sno ')\
        .replace('tnie ', 'tno ')\
        .replace('cznie ', 'czno ')\
        .replace('sznie ', 'szno ')\
        .replace('ynie ', 'yn ')\
        .replace('rznie ', 'rzno ')\
        .replace('nieźnie ', 'niezno ')\
        .replace('źnie ', 'zna ')\
        .replace('isie ', 'is ')\
        .replace('awie ', 'awa ')\
        .replace('czewie ', 'czów ')\
        .replace('niewie ', 'niew ')\
        .replace('szewie ', 'szew ')\
        .replace('ewie ', 'wów ')\
        .replace('kwie ', 'kwa ')\
        .replace('Ostrowie ', 'Ostrów ')\
        .replace('ewie ', 'ów ')\
        .replace('czowie ', 'czów ')\
        .replace('rowie ', 'rowa ')\
        .replace('owie ', 'ów ')\
        .replace('wie ', 'ów ')\
        .replace('gdzie ', 'gda ')\
        .replace('odzie ', 'oda ')\
        .replace('rdzie ', 'rd ')\
        .replace('jeździe ', 'jazd ')\
        .replace('orze ', 'ór ')\
        .replace('Górze ', 'Góra ')\
        .replace('cach ', 'ce ')\
        .replace('dach ', 'dy ')\
        .replace('chach ', 'chy ')\
        .replace('kach ', 'ki ')\
        .replace('lach ', 'le ')\
        .replace('nach ', 'ny ')\
        .replace('pach ', 'py ')\
        .replace('rach ', 'ry ')\
        .replace('wach ', 'we ')\
        .replace('dzach ', 'dze ')\
        .replace('żach ', 'że ')\
        .replace('kich ', 'kie ')\
        .replace('nych ', 'ne ')\
        .replace('rych ', 're ')\
        .replace('wych ', 'we ')\
        .replace('lii ', 'lia ')\
        .replace('rii ', 'ria ')\
        .replace('eli ', 'el ')\
        .replace('oli ', 'ola ')\
        .replace('czni ', 'cznia ')\
        .replace('lni ', 'lnia ')\
        .replace('Wsi ', 'Wieś ')\
        .replace('dwi ', 'dew ')\
        .replace('kwi ', 'kwia ')\
        .replace('odzi ', 'ódź ')\
        .replace('kiej ', 'ka ')\
        .replace('chej ', 'cha ')\
        .replace('niej ', 'nia ')\
        .replace('nej ', 'na ')\
        .replace('rej ', 'ra ')\
        .replace('wej ', 'wa ')\
        .replace('kim ', 'ki ')\
        .replace('nem ', 'ne ')\
        .replace('wym ', 'wy ')\
        .replace('żym ', 'ży ')\
        .replace('dcu ', 'dec ')\
        .replace('mcu ', 'miec ')\
        .replace('ńcu ', 'niec ')\
        .replace('wcu ', 'wiec ')\
        .replace('rzcu ', 'rzec ')\
        .replace('egu ', 'eg ')\
        .replace('rgu ', 'rg ')\
        .replace('omiu ', 'om ')\
        .replace('aniu ', 'ań ')\
        .replace('dniu ', 'deń ')\
        .replace('eniu ', 'eń ')\
        .replace('doniu ', 'doń ')\
        .replace('oniu ', 'óń ')\
        .replace('pniu ', 'pnie ')\
        .replace('uniu ', 'uń ')\
        .replace('yniu ', 'yń ')\
        .replace('awiu ', 'aw ')\
        .replace('iwiu ', 'iw ')\
        .replace('woju ', 'woj ')\
        .replace('iku ', 'ik ')\
        .replace('cku ', 'cko ')\
        .replace('czku ', 'czek ')\
        .replace('nku ', 'nek ')\
        .replace('ńsku ', 'ńsk ')\
        .replace('sku ', 'sko ')\
        .replace('tku ', 'tek ')\
        .replace('awku ', 'awek ')\
        .replace('jówku ', 'jówek ')\
        .replace('ówku ', 'ów ')\
        .replace('toku ', 'tok ')\
        .replace('chalu ', 'chale ')\
        .replace('walu ', 'wal ')\
        .replace('elu ', 'el ')\
        .replace('polu ', 'pol ')\
        .replace('olu ', 'ole ')\
        .replace('ślu ', 'śl ')\
        .replace('wlu ', 'wl ')\
        .replace('czu ', 'cz ')\
        .replace('rzu ', 'rz ')\
        .replace('szu ', 'sz ')\
        .replace('żu ', 'ż ')\
        .replace('icy ', 'ica ')\
        .replace('szczy ', 'szcz ')\
        .replace('czy ', 'cza ')\
        .replace('eży ', 'eż ')\
        .replace('mży ', 'mża ')
    print(place, ': ', nominative_place)
    return nominative_place


def nominative_from_genitive(place):
    if place is None:
        # print(place)
        return place
    else:
        place += ' '
    print(place)
    return place\
        .replace('nowa ', 'nów ')\
        .replace('ści ', 'ść ')\
        .replace('wicza ', 'wicz ')



def correct_place(place_str):
    #correct place name for special cases or db mistakes
    return place_str\
        .replace('Ogrodzie Sejmowym', 'Warszawa')\
        .replace('tamże pochowany','')\
        .replace('brak danych','')\
        .replace('(brak potwierdzenia w USC)','')\
        .replace(' prawdopodobnie','')\
        .replace('zamordowany ','')\
        .replace('rozstrzelany ','')\
        .replace('obóz pracy ','')\
        .replace('Ojciec Rudolf - pedagog','')\
        .replace('lub Wołkowysko ','')\
        .replace('Ujeżdzie','Ujazd')

def convert_place(place_str):
    if place_str:
        # clear empty chars and '-' at the begining and at the end
        place_str = place_str.strip().strip('-').strip()
        place_str = correct_place(place_str)

    tokens = place_str.split()
    if len(tokens) > 0 and (tokens[0] == 'w' or tokens[0] == 'we'):

        # Corect data

        pattern = '[a-zśćźżąęóńł\s]*([A-ZŚĆŹŻÓŃŁ][a-zśćźżąęóńł]+[\w\W]*$)'
        place = find_regex_value([pattern], place_str)
        converted = place;
        if place_str.find('obozie') > 0 or not place:
            converted = place
        elif len(tokens) > 2 and tokens[1] == 'okolicach':
            # TODO
            print("OKOLICE")
            print(place_str)
            print(place)
            nominative_place = nominative_from_genitive(place)
            converted = nominative_place.replace(' powiat', ', powiat')
        else:
            nominative_place = nominative_from_locative(place)
            # print(nominative_place)
            converted = nominative_place.replace(' powiat', ', powiat')
    else:
        converted = place_str
    if converted:
        converted = correct_place(converted)
    return converted


def get_place(string):

    extra_date_info_pattern = r'^[A-Z][a-z][\w\W]+\d{4}[\d\.]*\s?\([A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\s\.\d]+\)\??\,\s([A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s]+)[/;\,\.]'
    i_pattern = r'^[A-Z][a-z][a-zśćźżąęóńł\-\(\)\s\.\d]+\d{4}[\d\.]*\,?\s([A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s]+)\si[a-zśćźżąęóńł\-\(\)\s]*[pP]ochowan'
    month_string_pattern = r'^[A-Z][a-z][\w\W]+\d{4}\,[a-zśćźżąęóńł\s]*\,\s([A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s]+)[/;\,\.]'
    powiat_pattern = r'^[A-Z][a-z][\w\W]+\d{4}[\d\.]*\,?\s([A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s]+\,\spowiat\s[A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s]+)[/;\,\.]'
    w_pattern = r'^[A-Z][a-z][\w\W]+\d{4}[\d\.]*\s(we?\s[A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s\d]+)[/;\,\.]'
    standard_pattern = r'^[A-Z][a-z][\w\W]+\d{4}[\d\.]*\,\s[a-zśćźżąęóńł\-\(\)\s\d]*([A-ZŚĆŹŻÓŃŁ][A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s\d]+)[/;\,\.]'
    # no_date example:
    #   1. "Zm. - brak danych, Lwów." (Seib Tadeusz Józef 1887-?)
    #   2.
    no_date_pattern = r'^[UZ][a-z]\.[a-zśćźżąęóńł\-\(\)\s\,]*([A-ZŚĆŹŻÓŃŁ][A-ZŚĆŹŻÓŃŁa-zśćźżąęóńł\-\(\)\s\d]+)[/;\,\.]'

    patterns_list = [
        extra_date_info_pattern,
        i_pattern,
        month_string_pattern,
        powiat_pattern,
        w_pattern,
        standard_pattern,
        no_date_pattern,
    ]

    place_str = find_regex_value(patterns_list, string)
    if place_str and len(place_str) > 0:
        return convert_place(place_str)
    return None

def checkSejmValue(sejm_str):
     sejm_list = [
         "Sejm II RP. 1 kadencja (1922-1927)",
         "Sejm II RP. 2 kadencja (1928-1930)",
         "Sejm II RP. 3 kadencja (1930-1935)",
         "Sejm II RP. 4 kadencja (1935-1938)",
         "Sejm II RP. 5 kadencja (1938-1939)",
         "Sejm Ustawodawczy II RP (1919-1922)",
         "Senat II RP. 1 kadencja (1922-1927)",
         "Senat II RP. 2 kadencja (1928-1930)",
         "Senat II RP. 3 kadencja (1930-1935)",
         "Senat II RP. 4 kadencja (1935-1938)",
         "Senat II RP. 5 kadencja (1938-1939)"
     ]
     for sejm in sejm_list:
         if sejm == sejm_str:
             return True
     return None


def init_cleaner():
    import sys
    import csv
    from slugify import slugify

    EXTRACTED_CSV = 'sejm_ustawodawczy/extracted_sejm_ustawodawczy_ii_rp.csv'
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

                    obj[cell_header] = cell_str
                    obj['data-smierci'] = get_date(cell_str)
                    obj['miejsce-smierci'] = get_place(cell_str)

                elif cell_header == 'miejsce-i-rok-urodzenia':
                    cell_str = replace_abbreviations(cell)

                    obj[cell_header] = cell_str
                    obj['data-urodzenia'] = get_date(cell_str)
                    obj['miejsce-urodzenia'] = get_place(cell_str)

                elif cell_header == 'baza':
                    cell_content = cell.strip().strip('|')
                    baza_list = cell_content.split('|')
                    # print(baza_list)
                    for value in baza_list:
                        sejm = value.strip()
                        sejm_key = slugify(sejm)
                        if checkSejmValue(sejm):
                            obj[sejm_key] = 1
                elif cell_header == 'sejm':
                    obj['sejm-info'] = cell
                    tokens = cell.split()
                    if len(tokens) > 0 and tokens[0] == "Poseł":
                        obj['plec'] = "m"
                    elif len(tokens) > 0 and tokens[0] == "Posłanka":
                        obj["plec"] = "k"
                    else:
                        print("WARNING: no Posel/Poslanka. Check if man value")
                        print(row[0])
                        print("Sejm value: ", cell)
                        obj['plec'] = 'm'
                elif cell_header == 'senat':
                    obj['senat-info'] = cell
                else:
                    # print(stripNonAlphaNum(cell))
                    obj[cell_header] = cell

            results_list.append(obj)

    input_file.close()

#    print(results_list)
    save_to_csv(results_list, output_csv)

init_cleaner()