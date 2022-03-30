import json
import os

from docx import Document
from docxtpl import DocxTemplate
from thefuzz import fuzz, process


def create_cover_letter():
    table_contents = []
    
    print("Company Name:")
    company = input() or 'Test'
    
    # Reading New Requirements
    requirements_path = os.path.join(os.path.dirname(__file__),'requirements.txt')
    with open(requirements_path, 'r') as f:
        requirements = f.read().splitlines()
    
    # Archiving Requirements
    # archive_path = os.path.join(os.path.dirname(__file__),'archive_requirements.txt')
    # with open(archive_path, 'a') as f:
    #     for requirement in requirements:
    #         f.writelines('\n'+requirement)
    
    # Append appropriate responses to each requirement
    responses_path = os.path.join(os.path.dirname(__file__),'responses.json')
    with open(responses_path, 'r') as f:
        js_responses = json.load(f)
        
        for requirement in requirements:
            best_match = {'key':"",'requirement':"",'response':"",'max_ratio':0}
            for key,response in js_responses.items():
                ratio = fuzz.partial_ratio(key, requirement)
                if ratio > best_match['max_ratio']:
                    best_match['key'] = key
                    best_match['requirement'] = requirement
                    best_match['response'] = response
                    best_match['max_ratio'] = ratio

            table_contents.append(best_match)
    
    for element in table_contents:
        print(str(element)+'\n')
    # Import template document
    template = DocxTemplate('C://Users//Lee//Desktop//CoverLetterTemplate.docx')
    
    # Declare template variables
    context = {
        'company_name': company,
        'table_contents': table_contents,
    }

    # Render automated report
    template.render(context)
    cover_letter_directory = os.path.join(os.path.dirname(__file__),'Cover Letter.docx')
    template.save(cover_letter_directory)


create_cover_letter()
