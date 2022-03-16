import urllib
import webbrowser
from os.path import exists

import requests
from bs4 import BeautifulSoup

import get_job_postings
import get_links


def find_jobs(job_title, location, jobs):

    i = 0
    while True:
        job_postings = get_job_postings(job_title, location, i*10)
        i += 1

        links = get_links(job_postings)

        if len(links) > jobs:
            del links[jobs:len(links)]

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
                        # print("Added: ", link)
            else:
                for link in links:
                    file.write(link+'\n')

        links = list(filter(lambda x: x != '', links))

        if len(links) < jobs:
            continue

        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe  --profile-directory="Profile 3" %s'
        for link in links:
            if link != '':
                webbrowser.get(chrome_path).open(link)
        break


find_jobs("react developer", "los angeles", 5)
