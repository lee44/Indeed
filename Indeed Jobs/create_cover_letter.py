import os

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docxtpl import DocxTemplate


def create_cover_letter(url_links):

    path = os.path.join(os.path.dirname(__file__), 'config', 'key_words.txt')
    with open(path) as f:
        keyword_list = f.read().splitlines()

    for i, url in enumerate(url_links):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        job_title = soup.find('h1', class_="jobsearch-JobInfoHeader-title")
        company = soup.findAll('div', class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")[1]

        print(f"Generating cover letter for job with title {job_title.string} company {company.string}")

        job_description = soup.find('div', class_="jobsearch-jobDescriptionText")
        
        p_tags = job_description.find_all('p')

        for p_tag in p_tags:
            for keyword in keyword_list:
                if p_tag.find(text=keyword):
                    ul_tags = p_tag.nextSibling.nextSibling
                    
                    if ul_tags.find_all('b'):
                        b_tags = ul_tags.find_all('b')
                        
                        for b in b_tags:
                            print(b.string)
                    else:  
                        for li in ul_tags.find_all('li'):
                            print(li.string)
                elif isinstance(p_tag,Tag):
                    if p_tag.b:
                        if p_tag.string:
                            if p_tag.string.strip() == keyword:
                                ul_tags = p_tag.nextSibling
                                print(ul_tags)
                                if isinstance(ul_tags,Tag):
                                    if ul_tags.find_all('b'):
                                        b_tags = ul_tags.find_all('b')
                                        
                                        for b in b_tags:
                                            print(b.string)
                                    else:  
                                        for li in ul_tags.find_all('li'):
                                            print(li.string)
                                    break
            
        # requirements_index = 0
        # # Find index of <b> tag containing the words in requirement_key_words.txt
        # for index, tag in enumerate(filtered_list):
        #     if tag.b:
        #         for keyword in keyword_list:
        #             if keyword in tag.b.string.lower():
        #                 requirements_index = index + 1
        #                 break

        # if requirements_index != 0:
        #     li_tags = filtered_list[requirements_index]
        #     table_contents = []
        #     for child in li_tags.contents:
        #         if isinstance(child, Tag):
        #             table_contents.append({'Index': child.string})

        #     # Import template document
        #     template = DocxTemplate('C://Users//Lee//Desktop//CoverLetterTemplate.docx')

        #     # Declare template variables
        #     context = {
        #         'company_name': company.string,
        #         'table_contents': table_contents,
        #     }

        #     # Render automated report
        #     template.render(context)
        #     cover_letter_directory = os.path.join(os.path.dirname(__file__), 'Cover Letters', f'Cover Letter v{i}.docx')
        #     template.save(cover_letter_directory)


url_links = ['https://www.indeed.com/viewjob?cmp=Dev%7CViV&t=React+Js+Developer&jk=604455ca911818d6&q=Javascript+Developer&vjs=3']
create_cover_letter(url_links)
