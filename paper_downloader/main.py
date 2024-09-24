import time
import requests
from config import *
from components import *
import os
import warnings


warnings.simplefilter('ignore')


if __name__ == "__main__":
    papers = read_paper_titles_from_txt()
    for paper in papers:
        downloaded_or_not = exception_occurance(paper)
        if not downloaded_or_not:
            with open("paper_download_failed.txt", "a+") as fi:
                fi.write(paper + "\n")
        time.sleep(sleep_time)

# there are two ways to update this program
# traverse more google page
# put these methods into one class
# have a look at why it does not stop the program when the papers are downloaded