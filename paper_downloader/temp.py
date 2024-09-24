import requests
from config import *


base_url = "https://www.google.com/search?q="
query_string = "ViperGPT: Visual Inference via Python Execution for Reasoning"

url = base_url + query_string
response = requests.get(url)
# print(">>>", response)
print(">>>", response.text)
with open("output.html", "w") as out:
    out.write(response.text)