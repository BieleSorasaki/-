# PDFApi
import fitz
from PIL import Image
import pytesseract

import io
import os
import json

def extract_text_from_pdf_images(pdf_path, page_numbers=None):
    doc = fitz.open(pdf_path)
    if page_numbers is None:
        page_numbers = range(len(doc))
    for page_num in page_numbers:
        page = doc.load_page(page_num)
        images = page.get_images()
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = Image.open(io.BytesIO(base_image["image"]))
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return text

def get_filenames(folder_path, extensions=None, full_path=False):
    '''
    :param extensions: 过滤指定后缀以外的文件
    '''
    files = []
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            if extensions:
                if os.path.splitext(f)[1].lower() in extensions:
                    files.append(file_path if full_path else f)
            else:
                files.append(file_path if full_path else f)
    return files

def save_data(text: str = None, file_name: str = None):
    data = {
        "name": file_name,
        "data": text
    }
    with open("datas.json", 'a', encoding="utf-8") as fp:
        json.dump(data)

if __name__ == "__main__":
    extract_text_from_pdf_images("your_file.pdf", page_numbers=[0, 2])