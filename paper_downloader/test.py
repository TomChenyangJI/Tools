# import re
#
#
# s = "2406.16862"
# result = re.search("\d{3}", s)
# print(result.group())


from components import *
#
#
# res = google_search("Electrohydrodynamic jet printed photonic devices")
# #
# with open("temp.html", "w") as in_file:
#     in_file.write(res.text)


with open("temp.html", "r") as in_file:
    content = in_file.read()

from bs4 import BeautifulSoup


def extract_url(href: str):
    # this function is used to extract the pdf url in the <a> tag
    url = ""
    if ".pdf" in href and "http" in href:
        begin = href.find("http")
        end = href.find(".pdf")
        url = href[begin: end+4]
    return url


def get_all_urls_in_resp(resp):
    # two-layer deep search
    all_urls = []
    if "pdf" in resp.headers.get("content-type"):
        soup = BeautifulSoup(resp.text)
        a_li = soup.find_all("a")  # there might be exceptions here
        all_urls = []
        for a in a_li:
            href = a['href']
            url_li = href.split("http")
            url_li = ['http' + url for url in url_li]
            all_urls.extend(url_li)
        all_urls = list(set(all_urls))
    return all_urls


# arxiv > .pdf > normal links

soup = BeautifulSoup(content)
a_li = soup.find_all("a")
for a in a_li:
    # print(extract_url(a['href']).strip())
    # print(a['href'])
    href = a['href']
    urls = href.split("http")
    # print(urls)
    urls = ["http" + url for url in urls]
    print(urls)
    print()





