import fitz
import pandas as pd
import docx2txt
import ocrmypdf
from models.predict_class import CriteriaClassifier


model = CriteriaClassifier('models/criteria.json')


def word(file_path: str) -> str:
    return docx2txt.process(file_path)


def excel(file_path: str) -> str:
    xls = pd.ExcelFile(file_path)
    xls = xls.parse(0)

    text = ''
    for i, row in xls.iterrows():
        v = row.dropna().values
        if len(v) > 0:
            text += ' '.join(map(str, v)) + ' '
    return text


def pdf(file_path: str) -> str:
    file = fitz.open(file_path)
    text = ''
    for pageNum, page in enumerate(file.pages(), start=1):
        text += page.getText() + '\n'
    return text


def auto_conv(file_path: str) -> str:
    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        return pdf(file_path)
    elif file_type in ['docx', 'doc']:
        return word(file_path)
    elif file_type in ['xlsx', 'xls']:
        return excel(file_path)

    raise ValueError(f'Unsuppoted file type: {file_type}')


def predict(file_path: str):
    text = auto_conv(file_path)
    ocr = len(set(text)) == 1
    if ocr:
        ocrmypdf.ocr(file_path, 'files/buf.pdf', language=['rus'])
        text = auto_conv('files/buf.pdf').replace('\n', ' ')
    return model(text), ocr
