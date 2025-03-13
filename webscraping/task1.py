''' ■ PubmedID:Uniqueidentifier for the paper.
 ■ Title: Title of the paper.
 ■ Publication Date: Date the paper was published.
 ■ Non-academicAuthor(s): Names of authors affiliated with non-academic
 institutions.
 ■ CompanyAffiliation(s): Names of pharmaceutical/biotech companies.
 ■ Corresponding Author Email: Email address of the corresponding author'''
import requests
from bs4 import BeautifulSoup
import lxml
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
url_text="https://pubmed.ncbi.nlm.nih.gov/?term=reseach+paper"

requests.get(url_text,headers=headers) # request send

response = requests.get(url_text,headers=headers)
#requests.get(url_text,headers='headers')

#response = requests.get(url_text,headers=headers)

#print(response.status_code)
if response.status_code ==200:
    print("webscraping request accpected")
    soup= BeautifulSoup(response.text,"lxml")
    print(soup.prettify()[:1000])
else:
    print (f"not allowed :{response.status_code}")
    
