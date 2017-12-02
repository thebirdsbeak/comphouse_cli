'''
Command line program for grabbing company address company_details
'''

import click
from bs4 import BeautifulSoup
import requests
import pyperclip

@click.command()
@click.option('--c', prompt='Name', help='Name of UK entity.')
def company_details(c):
    '''Search for address, company number'''
    query = c.replace(' limited', '')
    query = query.replace(' plc', '')
    query = query.replace(' llp', '')
    record = []
    addresses = []
    companystrings = ''
    url = "https://beta.companieshouse.gov.uk/search/companies?q="+query

    data = requests.get(url)
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    for link in soup.find_all('a'):
        comp_option = str(link)
        if 'SearchSuggestions' in comp_option:
            comp_url = str(link.get('href'))
            comp_ref = comp_url.replace('/company/', '')
            namepart = str(link.contents).replace('<strong>', '').replace('</strong>', '').replace('[', '').replace(']', '').replace('\\n', '').replace(',', '').replace("'", '')
            namepart = ' '.join(namepart.split())
            nameoption = namepart.strip().lstrip()
            companystrings = nameoption
            record.append((companystrings, comp_ref))

    try:
        final_list = []
        for link in soup.find_all('p', class_=""):
            if "<strong" not in str(link) and "matches" not in str(link) and "<img" not in str(link):
                addresses.append(link.contents[0])
            information = list(zip(record, addresses))
        for i in information[0:10]:
            final_list.append("{}, {}, {}.".format(i[0][0], i[0][1], i[1]))
        for index, i in enumerate(final_list):
            print("{} - {}".format(index, i))
        copy = input("Copy > ")
        try:
            copy = int(copy)
            pyperclip.copy(final_list[copy])
        except:
            return
        else:
            return
    except:
        return "No companies found!"
    else:
        return

if __name__ == '__main__':
    company_details()
