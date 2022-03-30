import urllib

import requests
from bs4 import BeautifulSoup


def get_job_postings(job_title, location, page):
    # First page on Indeed doesn't have a "start" url parameter
    if page == 0:
        url_param = {'q': job_title, 'l': location,
                     'explvl': "entry_level", 'fromage': "14"}
    else:
        url_param = {'q': job_title, 'l': location,
                     'start': page, 'explvl': "entry_level", 'fromage': "7"}

    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(url_param))
    print("Searching... ", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find('div', id="mosaic-provider-jobcards")
    return job_soup

get_job_postings("react developer", "los angeles", 5)
