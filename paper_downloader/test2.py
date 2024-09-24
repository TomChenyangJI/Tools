import requests
import urlvalidator


url = "https://nano.ece.illinois.edu/files/2017/11/128.pdf%26hl%3Dzh-TW%26sa%3DX%26ei%3DfufuZs6JEOiB6rQPq73xgQk%26scisig%3DAFWwaeY6J7FSYFX6q54xh6-MBNHE%26oi%3Dscholarr&sa=U&ved=2ahUKEwinga-ertSIAxXSn68BHY4HHWMQgAN6BAgJEAM&usg=AOvVaw3RtgJFgzra-h34R2nPq-Rz"

# res = requests.get(url)
# print(res.headers.get("content-type"))
# url = 'http/setprefs?hl=zh-TW&prev='
# validate = urlvalidator.URLValidator()
#
# validate(url)


def valid_url_or_not(url):
    validate = urlvalidator.URLValidator()
    try:
        validate(url)
        return True
    except urlvalidator.ValidationError:
        return False


from PyPDF2 import PdfReader


# reader = PdfReader("./Barton/Predictive Modeling of Human Fatigue in a Manufacturing-Like Setting.pdf")
# print(reader.pages)


def get_pdf_content(file):
    from PyPDF2 import PdfReader
    reader = PdfReader(file)
    pages = reader.pages
    content = ""
    txt = pages[0].extract_text()
    txt = txt.replace("\n", " ")
    paper = "Correct-by-construction adaptive cruise control: Two approaches"
    # print("Correct-By-Construction Adaptive Cruise Control: Two Approaches" == paper, " <<< ")
    # print(txt[:len(txt)//3], " << ")
    # print(txt)
    # print(txt[:len(txt)//2])
    for page in pages:
        content += page.extract_text()
    content = content.replace("\n", " ")
    with open("pdf_content.txt", "w") as fi:
        fi.write(content)
    return content

paper = "Correct-by-construction adaptive cruise control: Two approaches"

# print(paper in get_pdf_content("./Barton/Correct-by-construction_adaptive_cruise_control__Two_approaches.pdf"))
# import time
# import datetime
# start = time.strftime("%s")
# end = time.strftime("%s")
# print(float(end) - float(start))

import re

s = "pdf/2208.11739"
# print(re.search("\d{4}\.\d{2,10}", s).group())


def is_right_paper(save_path, paper):
    # in this function , i need to check if the pdf downloaded is the right paper i want to download
    content = get_pdf_content(save_path)

    import unicodedata
    # this is for the wrong recognition of letters in PDF
    content = unicodedata.normalize("NFKD", content)

    if paper.lower() in content.lower():
        return True
    return False


print(is_right_paper("./Lionel Robert/2208.11739v1.pdf",
                     "Rethinking Cost-Sensitive Classification in Deep Learning via Adversarial Data Augmentation"))