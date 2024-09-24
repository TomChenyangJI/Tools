import time
import requests
from config import *
from components import *
import os
import warnings


warnings.simplefilter('ignore')


# if __name__ == "__main__":
#     papers = read_paper_titles_from_txt()
#     try:
#         delete_file("paper_download_failed.txt")
#     except FileNotFoundError:
#         pass
#
#     for paper in papers:
#         downloaded_or_not = exception_occurance(paper)
#         if not downloaded_or_not:
#             with open("paper_download_failed.txt", "a+") as fi:
#                 fi.write(paper + "\n")
#         time.sleep(sleep_time)


def target_function(paper):
    downloaded_or_not = exception_occurance(paper)
    if not downloaded_or_not:
        with open("paper_download_failed.txt", "a+") as fi:
            fi.write(paper + "\n")
    time.sleep(sleep_time)


from multiprocessing import Pool


if __name__ == '__main__':
    papers = read_paper_titles_from_txt()
    with Pool(cores) as p:
        print(p.map(target_function, papers))


# there are two ways to update this program
# traverse more google page
# put these methods into one class
# have a look at why it does not stop the program when the papers are downloaded