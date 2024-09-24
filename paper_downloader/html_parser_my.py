from bs4 import BeautifulSoup
from components import *

paper_title = "ViperGPT: Visual Inference via Python Execution for Reasoning"
pdf_base_file = "./"
with open("output.html", "r") as inp:
    content = inp.read()

soup = BeautifulSoup(content, features="html.parser")
body = soup.find("body")

# <div id="main">

main_div = body.find("div", attrs={"id": "main"})

# <div class="Gx5Zad xpd EtOod pkphOe">
block_divs = main_div.find_all("div", attrs={"class": "Gx5Zad xpd EtOod pkphOe"})

divs_checked = []
for div in block_divs:
    # div class="BNeawe vvjwJb AP7Wnd">
    page_title = div.find("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"})

    if page_title is not None:
        divs_checked.append(div)

# print(divs_checked)
# arxiv link first because there are so many papers published on this website
arxiv_title_li = filter(arxiv_filter, divs_checked)
# print(list(arxiv_title_li))
for arxiv_title in arxiv_title_li:
    page_url = get_arxiv_url_from_div(arxiv_title)
    print(page_url)
    if page_url != "":  # means I got the Arxiv link
        if "pdf" in page_url:
            # download the pdf directly.
            download_pdf(page_url, pdf_base_file+paper_title)
            break
        # print(page_url)

# other origins, some other websites, including the paper than I can download directly from Google result
# for div in block_divs:
#     # div class="BNeawe vvjwJb AP7Wnd">
#     page_title = div.find("div", attrs={"class": "BNeawe vvjwJb AP7Wnd"})
#
#     if page_title is not None:
#         page_title = page_title.text
#         if match_strs(page_title, paper_title):  # means they match.
#             pass
#
#         # print(page_text)
#     a_tags = div.find_all_next("a")
#     for a in a_tags:
#         href = a["href"]
#         try:
#             inx = href.index("https")
#         except ValueError:
#         # inner_url = href[inx:]  # this is the page link
#             pass
#


# TODO
"""
add multithread of this program
put the title of the files into a text file for better maintenance

"""