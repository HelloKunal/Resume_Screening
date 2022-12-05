import textract
import re
from resume_rating import image_handler, ppt_handler

def get_content_as_string(filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        lower_case_string = image_handler.image_to_string(filename).lower()
    elif filename.lower().endswith(('pptx', 'pptm', 'ppt')):
        lower_case_string = ppt_handler.ppt_to_string(filename).lower()
    else:
        text = textract.process(filename)
        lower_case_string =  str(text.decode('utf-8')).lower()
    #final_string = re.sub('[^a-zA-Z0-9 \n]', '', lower_case_string)
    print(lower_case_string)
    return lower_case_string