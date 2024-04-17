import fitz 
import json


def extract_headings_and_contents(
    pdf_paths, red_color = 14176347 , 
    grey_color = 8287858) :

    headings_contents = {}
    current_heading = None
    current_content = ''

    for path in pdf_paths : 

        doc = fitz.open(path)

        for page in doc : 

            blocks = page.get_text('dict')['blocks']

            for block in blocks :

                try :  

                    for line in block['lines'] : 

                        try :

                            for span in line['spans'] : 

                                try : 

                                    color = span['color']
                                    text = span['text']
                                    size = span['flags']

                                    if color == red_color or size & 1 << 5 : 

                                        if current_heading : 

                                            if current_heading in headings_contents : headings_contents[current_heading] += current_content.strip() + '\n' 
                                            else : headings_contents[current_heading] = current_content.strip()

                                        current_heading = text
                                        current_content = ''

                                    else : current_content += text + ''

                                except : pass
                        except : pass
                except : pass
        if current_heading : 

            if current_heading in headings_contents : headings_contents[current_heading] += current_content.strip() 
            else : headings_contents[current_heading] = current_content.strip()

    return headings_contents

sections = extract_headings_and_contents([
    'Assets/PDFs/input_pdf_20.pdf' , 
    'Assets/PDFs/pzuw- 1 column.pdf' , 
    'Assets/PDFs/SWU_WDCiR_2014_02 - 1 column.pdf'
])


json_data = json.dumps(sections)

with open('Assets/JSONs/data.json' , 'w') as fil : json.dump(json_data, fil)