import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docxtpl import DocxTemplate


def generate_cover_letter(url_links):
    
    for index,url in enumerate(url_links):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        job_title = soup.find('h1', class_="jobsearch-JobInfoHeader-title")
        company = soup.find('div', class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")
    
        print(f"Generating cover letter for job with title {job_title.string} company {company.string}")
        
        job_description = soup.find('div', class_="jobsearch-jobDescriptionText")
        
        # Filter \n elements from list
        filter_list = list(filter(lambda x: x != '\n', job_description.contents))
        
        # Find index of <b> tag containing the word requirement or qualification
        for index,tag in enumerate(filter_list):
            if tag.b:
                if 'requirement' in tag.b.string.lower() or 'qualification' in tag.b.string.lower():
                    requirements_index = index + 1
                    break
                
        li_tags = filter_list[requirements_index]
        table_contents = []
        for child in li_tags.contents:
            if isinstance(child,Tag):   
                table_contents.append({'Index':child.string})
                    
        # Import template document
        template = DocxTemplate('C://Users//Lee//Desktop//CoverLetterTemplate.docx')

        # Declare template variables
        context = {
            'company_name': company,
            'table_contents': table_contents,
        }

        # Render automated report
        template.render(context)
        template.save(f'Cover Letter v{index}.docx')

url_links = ['https://www.indeed.com/viewjob?jk=6f37f1225cfa3930&q=react&l=United+States&tk=1fuv3t4pb30a3000&from=web&advn=9860451091899549&adid=386415654&ad=-6NYlbfkN0BrPeHrFMQVOEU3cJhS7IRk6FDr0fwccUOvJL73GNlbZ8GjUIewXmSksqSioNLjSUnV6UKzwvFjVxoCB4PvFrNXS69Uqj0KP5mOT6M8VAI8jpgb3it1Xy5Yx05aik3fFWWnhGaxnUsAIu47-yyu1hR3cCAQQE0LuarXW52UQS5purcxUTDT_z43VNybpu_GDPVVmwJ8_qZI5ufKJtfaLXK6qnHiHALHCqkaJoD0cRachq5uvJD2LO0-UO938no3HgVEm0TKSiREbp2h7vnu99XGOV0JVPiSv2Qa5ENI8zRKxEsEHd3XuNP1t_72qpV5mjZUmKyg3u5UGCkWFVchIH0iAcOTUwfAJ31Rcj0J0VYa7pH38IJSRIlp&pub=4a1b367933fd867b19b072952f68dceb&vjs=3']
generate_cover_letter(url_links)
