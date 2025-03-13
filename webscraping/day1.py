import requests
from bs4 import BeautifulSoup
import csv
url="https://www.bikewale.com/royalenfield-bikes/hunter-350/"
page = requests.get(url)
soup = BeautifulSoup(page.content,"html.parse")
print(soup.text)