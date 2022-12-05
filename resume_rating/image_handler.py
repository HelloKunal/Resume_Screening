from PIL import Image
import pytesseract

def process_image(iamge_name, lang_code):
	return pytesseract.image_to_string(Image.open(iamge_name), lang=lang_code)

def print_data(data):
	print(data)

# def output_file(filename, data):
# 	file = open(filename, "w+")
# 	file.write(data)
# 	file.close()

def image_to_string(document_path, language="eng"):
	data_eng = process_image(document_path, language)
	print_data(data_eng)
	return data_eng
