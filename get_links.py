def getLinks(job_soup):
    job_elems = job_soup.find_all('a', class_="tapItem")

    links = []

    for job_elem in job_elems:
        links.append(append_link(job_elem))

    return links


def append_link(job_elem):
    link = 'www.Indeed.com' + job_elem['href']
    return link
