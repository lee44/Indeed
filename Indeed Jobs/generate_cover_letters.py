import os

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docxtpl import DocxTemplate


def generate_cover_letter(url_links):
    
    path = os.path.join(os.path.dirname(__file__),'config','requirement_key_words.txt')
    with open(path) as f:
        keyword_list = f.read().splitlines()
    
    for i,url in enumerate(url_links):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        job_title = soup.find('h1', class_="jobsearch-JobInfoHeader-title")
        company = soup.findAll('div', class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")[1]
        
        print(f"Generating cover letter for job with title {job_title.string} company {company.string}")
        
        job_description = soup.find('div', class_="jobsearch-jobDescriptionText")
        
        # Filter \n elements from list
        filtered_list = list(filter(lambda x: x != '\n', job_description.contents))
        
        requirements_index = 0
        # Find index of <b> tag containing the words in requirement_key_words.txt
        for index,tag in enumerate(filtered_list):
            if tag.b:
                for keyword in keyword_list:
                    if keyword in tag.b.string.lower():
                        requirements_index = index + 1
                        break
        
        if requirements_index != 0:
            li_tags = filtered_list[requirements_index]
            table_contents = []
            for child in li_tags.contents:
                if isinstance(child,Tag):   
                    table_contents.append({'Index':child.string})
                        
            # Import template document
            template = DocxTemplate('C://Users//Lee//Desktop//CoverLetterTemplate.docx')
            
            # Declare template variables
            context = {
                'company_name': company.string,
                'table_contents': table_contents,
            }

            # Render automated report
            template.render(context)
            cover_letter_directory = os.path.join(os.path.dirname(__file__),'Cover Letters',f'Cover Letter v{i}.docx')
            template.save(cover_letter_directory)

url_links = ['https://www.indeed.com/viewjob?cmp=Exponentlogic-Solution&t=Javascript+React+Developer&jk=417811ecf02b9ece&q=react+developer&vjs=3']
generate_cover_letter(url_links)
