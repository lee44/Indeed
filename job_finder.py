import urllib
import webbrowser
from os.path import exists

import requests
from bs4 import BeautifulSoup


def find_jobs(job_title, location, jobs):

    i = 0
    while True:
        job_soup = load_indeed_jobs(job_title, location, i*10)
        i += 1

        links = getLinks(job_soup)

        if not(exists('applied.txt')):
            open('applied.txt', 'x')

        with open('applied.txt', 'r') as file:
            lines = file.readlines()

        with open('applied.txt', 'a') as file:
            if(len(lines) != 0):
                for index, link in enumerate(links):
                    if link+'\n' in lines:
                        links[index] = ''
                    else:
                        file.write(link+'\n')
                        print("Added: ", link)
            else:
                for link in links:
                    file.write(link+'\n')

        links = list(filter(lambda x: x != '', links))

        if len(links) < jobs:
            continue
        elif len(links) > jobs:
            del links[jobs:len(links)]

        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe  --profile-directory="Profile 3" %s'
        for link in links:
            if link != '':
                webbrowser.get(chrome_path).open(link)
        break


def load_indeed_jobs(job_title, location, page):
    # First page on Indeed doesn't have a "start" url parameter
    if page == 0:
        url_param = {'q': job_title, 'l': location}
    else:
        url_param = {'q': job_title, 'l': location, 'start': page}

    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(url_param))
    print("Searching... ", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find('div', id="mosaic-provider-jobcards")
    return job_soup


def getLinks(job_soup):
    job_elems = job_soup.find_all('a', class_="tapItem")

    links = []

    for job_elem in job_elems:
        links.append(extract_link(job_elem))

    return links


def extract_link(job_elem):
    link = 'www.Indeed.com' + job_elem['href']
    return link


find_jobs("software internship", "united states", 10)
