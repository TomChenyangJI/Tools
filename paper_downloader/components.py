import os
import time

import urlvalidator
from bs4 import BeautifulSoup

from config import *
import re
import requests


arxiv_urls = []
pdf_search_method_urls = []
traversal_searched_urls = []


def is_pdf_content_type(res):
    if "pdf" in res.headers.get("content-type"):
        return True
    return False


def delete_file(file):
    os.remove(file)


def get_all_arxiv_urls(all_urls):
    all_arxiv_urls = []
    for url in all_urls:
        if url and "arxiv" in url.lower():
            all_arxiv_urls.append(url)
    return all_arxiv_urls


def download_pdf(url, file_name="paper_name", trial=0):
    print("\turl is ", url)
    if trial < 3:
        # this function will try to download the pdf 3 times at most in case the exception happens in the progress
        try:
            import requests
            # with requests.get(url, verify=False, stream=True) as response:
            with requests.get(url, verify=False) as response:
                if response.status_code == 200:
                    file_name = file_name.strip().replace(":", " ")
                    with open(file_name, "wb") as file:
                        # for chunk in response.iter_content(chunk_size=8192):
                        #     if chunk:
                        #         file.write(chunk)
                        file.write(response.content)

                    return True
                else:
                    raise Exception("invalid response")
        except Exception as e:
            time.sleep(sleep_time)
            print("download_pdf error: ", e)
            return download_pdf(url, file_name, trial+1)
    else:
        return False


def read_paper_titles_from_txt(in_file="./papers_to_be_downloaded.txt"):
    with open(in_file, "r") as fi:
        lines = fi.readlines()
        papers = [line.strip() for line in lines if line.strip()]
    return papers


def google_search(q):
    url = base_url + q
    response = requests.get(url, verify=False, cookies=cookies, headers=headers)
    return response


def form_arxiv_url(url):
    # print(" form arxiv url is ", url)
    patter = "\d{4}\.\d{2,10}"
    search_result = re.search(patter, url)
    if search_result:
        return "https://arxiv.org/pdf/" + search_result.group()
    return ""


def is_title_in_content(paper, content):
    paper_title_split = paper.lower().split(" ")
    paper_title_split = [ele.strip() for ele in paper_title_split if ele.strip() != ""]
    content_lower = content.lower()
    inx = content_lower.index(paper_title_split[0])
    l = len(paper)
    conta_str = content_lower[inx: inx + l * 10 + 1]
    count = 0
    for ele in paper_title_split:
        if ele in conta_str:
            count += 1
    if count / len(paper_title_split) >= match_threshold:
        return True
    else:
        return False


def is_right_paper(save_path, paper):
    # in this function , i need to check if the pdf downloaded is the right paper i want to download
    content = get_pdf_content(save_path)
    import unicodedata
    # this is for the wrong recognition of letters in PDF
    content = unicodedata.normalize("NFKD", content)
    return is_title_in_content(paper, content)


def get_arxiv_abstract_html_url(url):
    abstract_html = url.replace("pdf", "abs")
    return abstract_html


def is_right_arxiv_paper(arxiv_pdf_url, paper):
    abstract_html_url = get_arxiv_abstract_html_url(arxiv_pdf_url)
    abstract_res = get_request(abstract_html_url)
    time.sleep(sleep_time)
    if abstract_res.status_code == 200:
        abstract_text = abstract_res.text
        abstract_soup = BeautifulSoup(abstract_text)
        body_tag = abstract_soup.find("body")
        abstract_text = body_tag.text
        abstract_text = abstract_text.replace("\n", " ")
        import unicodedata
        content = unicodedata.normalize("NFKD", abstract_text)
        return is_title_in_content(paper, content)
    else:
        return False


def arxiv_filtered_downloader(all_arxiv_urls:list, pdf_save_path, paper):
    # arxiv link first because there are so many papers published on this website
    global arxiv_urls
    for page_url in all_arxiv_urls:
        time.sleep(sleep_time)
        try:
            arxiv_urls.append(page_url)
            arxiv_pdf_url = form_arxiv_url(page_url)
            print("\t arxiv url:  ", arxiv_pdf_url)
            if arxiv_pdf_url != "" and is_right_arxiv_paper(arxiv_pdf_url, paper):
                result = download_pdf(arxiv_pdf_url, pdf_save_path)
                if result:
                    print("arxiv method succeeded")
                    return True
        except Exception:
            continue
    print("arxiv method failed")
    return False


def extract_pdf_url(href: str):
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
    soup = BeautifulSoup(resp.text)
    a_li = soup.find_all("a")  # there might be exceptions here
    all_urls = []
    for a in a_li:
        try:
            href = a['href']
            url_li = href.split("http")
            url_li = ['http' + url for url in url_li]
            all_urls.extend(url_li)
        except Exception:
            continue

    all_urls = list(set(all_urls))
    return all_urls


def create_pdf_save_base_path():
    if professor_name:
        temp_path = os.path.join(pdf_base_path, professor_name)
        os.makedirs(temp_path, exist_ok=True)
        return temp_path
    os.makedirs(base_url, exist_ok=True)
    return base_url


def valid_url(url):
    validate = urlvalidator.URLValidator()
    try:
        validate(url)
        return True
    except urlvalidator.ValidationError:
        return False


def get_pdf_content(file):
    from PyPDF2 import PdfReader
    reader = PdfReader(file)
    pages = reader.pages
    content = ""
    for page in pages[: len(pages)//3]:
        content += page.extract_text()
    content = content.replace("\n", " ")
    return content


def get_request(url, params=None):
    return requests.get(url, verify=False, cookies=cookies, headers=headers, params=params)


def traversal_search_downloader_new(all_traversal_urls, save_path, paper):
    for url in all_traversal_urls:
        time.sleep(sleep_time)
        try:
            resp = get_request(url)
            traversal_searched_urls.append(url)
            if is_pdf_content_type(resp):
                result = download_pdf(url, save_path)
                if result:
                    if is_right_paper(save_path, paper):
                        print("traversal method succeeded")
                        return True
                    else:
                        delete_file(save_path)
        except Exception:
            continue
    return False


def get_initial_depth_search_urls(all_urls, arxiv_urls, pdf_urls):
    init_urls = []
    for url in all_urls:
        if url not in arxiv_urls and url not in pdf_urls and url not in redundant_urls:
            init_urls.append(url)
    return init_urls


def get_all_pdf_urls(all_urls):
    all_pdf_urls = []
    for url in all_urls:
        extracted_url = extract_pdf_url(url)
        all_pdf_urls.append(extracted_url)

    return all_pdf_urls


def pdf_url_extractor_downloader(all_pdf_urls, save_path, paper):
    for pdf_url in all_pdf_urls:
        time.sleep(sleep_time)
        try:
            if valid_url(pdf_url):
                result = download_pdf(pdf_url, save_path)  # this method is not safe
                if result and is_right_paper(save_path, paper):
                    print("pdf method succeeded")
                    return True
        except Exception:
            continue

    print("pdf method failed")
    return False


def get_all_traversal_urls(all_urls):
    all_traversal_urls = []
    for url in all_urls:
        if url not in arxiv_urls and url not in pdf_search_method_urls and url not in redundant_urls:
            all_traversal_urls.append(url)
    return all_traversal_urls


def download_paper(paper, all_urls):
    global pdf_search_method_urls

    pdf_base_path = create_pdf_save_base_path()
    paper_cp = paper.replace(":", "_")
    paper_cp = paper_cp.replace(" ", "_")
    save_path = os.path.join(pdf_base_path, paper_cp)
    save_path += ".pdf"
    # 1. arxiv first
    try:
        all_arxiv_urls = get_all_arxiv_urls(all_urls)
        arxiv_done = arxiv_filtered_downloader(all_arxiv_urls, save_path, paper)
    except Exception:
        arxiv_done = False

    pdf_download_success: bool
    all_pdf_urls = []
    if arxiv_done:
        return arxiv_done
    else:
        # it means there is no valid arxiv link on the first page
        # 2. then .pdf search
        all_pdf_urls = get_all_pdf_urls(all_urls)
        pdf_download_success = pdf_url_extractor_downloader(all_pdf_urls, save_path, paper)

    if pdf_download_success:
        return True
    else:
        pdf_search_method_urls.extend(all_pdf_urls)

    traversal_search_success = False
    if not pdf_download_success:
        # 3. if .pdf search fails again, then the mass search
        # it means this function doesn't download the paper either
        # when this happens, i need to use the depth search to download the paper
        all_traversal_urls = get_all_traversal_urls(all_urls)
        traversal_search_success= traversal_search_downloader_new(all_traversal_urls, save_path, paper)

    return traversal_search_success


def depth_search(init_urls: list, paper, recu=0):
    # print("\tdepth search init urls: ", init_urls)
    if recu <= max_recursion:
        result = False
        for url in init_urls:
            time.sleep(sleep_time)
            res = get_request(url)
            all_urls = get_all_urls_in_resp(res)
            success = download_paper(paper, all_urls)
            if success:
                return True
            else:
                time.sleep(sleep_time)
                result = depth_search(all_urls, paper, recu+1)
                if result:
                    break
        return result
    else:
        return False


#https://www.google.com/search?q=test&start=10
def download_paper_wrapper(paper, recu=0):
    if 0 <= recu <= max_recursion:
        try:
            if recu == 0:
                print(paper)
            res = get_request("https://www.google.com/search", params={"q": paper, "start": str(recu * 10)})
            all_urls = get_all_urls_in_resp(res)

            with open("temp.html", "w") as fi:
                fi.write(res.text)
            download_succcess = download_paper(paper, all_urls)
            depth_search_success = False
            if download_succcess:
                return True
            else:  # depth search
                print("depth serach start...")
                depth_search_success = depth_search(all_urls, paper)
            if depth_search_success:
                return True
            else:
                time.sleep(sleep_time)
                return download_paper_wrapper(paper, recu+1)  # search the different pages of Google return pages
        except Exception:
            time.sleep(sleep_time)
            return download_paper_wrapper(paper, recu+1)
    else:
        return False


def exception_occurance(paper, recu_times=0):
    try:
        if recu_times < 5:
            result = download_paper_wrapper(paper)
            return result
        return False
    except requests.exceptions.ChunkedEncodingError or requests.exceptions.ConnectionError or Exception:
        time.sleep(sleep_time)
        exception_occurance(paper, recu_times+1)

# TODO
# the only thing i need do is to polish the get_all_url method, which i may put the concatenating feature into this function
# maybe another thing i can do is to put all these functions into a class, so as to remove the global variables
