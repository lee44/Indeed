import os
import webbrowser
from doctest import script_from_examples
from os.path import exists

from bs4 import BeautifulSoup

from generate_cover_letters import generate_cover_letter
from get_job_postings import get_job_postings
from get_links import get_links


# cd env/Scripts
# . activate
def find_jobs(job_title, job_location='United States', job_limit=10):

    i = 0
    jobs_applied = os.path.join(os.path.dirname(__file__),'jobs_applied.txt')
    while True:
        job_postings = get_job_postings(job_title, job_location, i)
        i += 1

        url_list = get_links(job_postings)

        # If the length of url_list exceeds job_limit, delete all indexes after the job_limit so length of url_list matches job_limit
        if len(url_list) > job_limit:
            del url_list[job_limit:len(url_list)]

        # Creates a file if it doesn't exists
        if not(exists(jobs_applied)):
            open(jobs_applied, 'x')

        with open(jobs_applied, 'r') as file:
            lines = file.readlines()

        with open(jobs_applied, 'a') as file:
            # if jobs_applied file is not empty, check if link exists inside file
            if(len(lines) != 0):
                for index, link in enumerate(url_list):
                    if link + '\n' in lines:
                        url_list[index] = ''
                    else:
                        file.write(link + '\n')

            # # if jobs_applied file is empty, append link to file
            else:
                for link in url_list:
                    file.write(link + '\n')

        # Filters any empty indexes in the list
        url_list = list(filter(lambda x: x != '', url_list))

        if len(url_list) < job_limit:
            continue
        
        generate_cover_letter(url_list)

        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe  --profile-directory="Profile 3" %s'
        for link in url_list:
            if link != '':
                webbrowser.get(chrome_path).open(link)
        break


find_jobs("react developer", "los angeles", 5)
