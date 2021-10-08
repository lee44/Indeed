import datetime
import urllib
import webbrowser

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def find_jobs(job_title, location, pages):

    results = []
    i = 0
    while i < pages:
        job_soup = load_indeed_jobs_div(job_title, location, i*10)
        results.append(extract_job_info(job_soup))
        i += 1

    titles = []
    companies = []
    links = []
    age = []
    for page in results:
        if list(page.keys())[0] == 'titles':
            titles.append(page['titles'])
        if list(page.keys())[1] == 'companies':
            companies.append(pages['companies'])
        if list(page.keys())[2] == 'links':
            links.append(page['links'])
        if list(page.keys())[3] == 'age':
            age.append(page['age'])

    numpyTitles = np.asarray(titles)
    numpyCompanies = np.asarray(companies)
    numpyLinks = np.asarray(links)
    numpyAge = np.asarray(age)

    excel = {}
    excel['titles'] = numpyTitles.flatten()
    excel['companies'] = numpyCompanies.flatten()
    excel['links'] = numpyLinks.flatten()
    excel['age'] = numpyAge.flatten()

    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe  --profile-directory="Profile 3" %s'

    for link in excel['links']:
        webbrowser.get(chrome_path).open(link)

    # dateTime = datetime.datetime.now()
    # filename = "results {}-{}-{}.xlsx".format(
    #     dateTime.month, dateTime.day, dateTime.year)
    # save_jobs_to_excel(excel, filename)

## ================== FUNCTIONS FOR INDEED =================== ##


def load_indeed_jobs_div(job_title, location, page):
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


def extract_job_info(job_soup):
    job_elems = job_soup.find_all('a', class_="tapItem")

    cols = []
    extracted_info = []

    titles = []
    cols.append('titles')
    for job_elem in job_elems:
        titles.append(extract_job_title_indeed(job_elem))
    extracted_info.append(titles)

    companies = []
    cols.append('companies')
    for job_elem in job_elems:
        companies.append(extract_company_indeed(job_elem))
    extracted_info.append(companies)

    links = []
    cols.append('links')
    for job_elem in job_elems:
        links.append(extract_link_indeed(job_elem))
    extracted_info.append(links)

    dates = []
    cols.append('age')
    for job_elem in job_elems:
        dates.append(extract_date_indeed(job_elem))
    extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    return jobs_list


def extract_job_title_indeed(job_elem):
    h2_elem = job_elem.find('h2', class_='jobTitle')
    title_elem = h2_elem.findChildren('span', recursive=True)
    title = title_elem[len(title_elem)-1].text
    return title


def extract_company_indeed(job_elem):
    span_elem = job_elem.find('span', class_='companyName')
    company_elem = span_elem.findChildren('a', recursive=False)
    if(len(company_elem) > 0):
        return company_elem[len(company_elem)-1].text
    return ""


def extract_link_indeed(job_elem):
    link = 'www.Indeed.com' + job_elem['href']
    return link


def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text
    return date

## ======================= GENERIC FUNCTIONS ======================= ##


def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename, index=False, header=True)

## ================================================================= ##


find_jobs("software internship", "united states", 1)
