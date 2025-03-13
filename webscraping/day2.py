# This app scrap data from bookong .com

'''
give the url , file name
greetings
start scrapping
hotel_name
price
location
rating
reviewa
links
save the file

'''

import requests
from bs4 import BeautifulSoup
import lxml
import csv
import time

#url_text = 'https://www.booking.com/searchresults.html?ss=New+Delhi%2C+Delhi+NCR%2C+India&ssne=Hyderabad&ssne_untouched=Hyderabad&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaGyIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AtSF670GwAIB0gIkOWQyOWM4ZmEtNDJiMy00YjBmLWFjNWYtMDAwNGY5ZjAzY2Mw2AIF4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2106102&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=40742efe18550314&ac_meta=GhA0MDc0MmVmZTE4NTUwMzE0IAAoATICZW46A25ld0AASgBQAA%3D%3D&checkin=2025-04-01&checkout=2025-04-02&group_adults=2&no_rooms=1&group_children=0'



#requests.get(url_text,headers='headers')

#response = requests.get(url_text,headers=headers)

#print(response.status_code)

def web_scraper1(web_url,f_name):
  
  #greetings
  print("Thank you sharing the url and file name ! \n Reading web page...\n web scrapping")

  #processing
  time.sleep(5)

  headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'}
  response = requests.get(web_url,headers=headers)

  if response.status_code == 200:
    print("connected to the website")
    html_content = response.text
   #  print(response.text)

    #creating soup
    soup = BeautifulSoup(html_content,'lxml')

    #print(soup.prettify())

    hotel_divs = soup.find_all('div',role="listitem")
    
    with open(f'{f_name}.csv','w',encoding='utf-8') as file_csv:
      writer = csv.writer(file_csv)

      #adding header
      writer.writerow(['hotel_name','locality','price','review','rating','link'])
      #print(hotel_divs)
      for hotel in hotel_divs:
        hotel_name=hotel.find('div',class_="f6431b446c a15b38c233").text.strip()
        hotel_name if hotel_name else "na"
        location = hotel.find('span',class_="aee5343fdb def9bc142a").text.strip()
        location if location else "na"
        price = hotel.find('span',class_="f6431b446c fbfd7c1165 e84eb96b1f").text.strip().replace('₹ ','')
        price if price else "na"
        review =hotel.find('div',class_="abf093bdfe f45d8e4c32 d935416c47").text.strip().split(' ')[0]
        review if review else "na"
        rating = hotel.find('div',class_="a3b8729ab1 d86cee9b25").text.strip().split(' ')[-1]
        rating if rating else "na"
        link = hotel.find('a',href=True).get('href')
        link if link else "na"
        # saving the file 
        writer.writerow([hotel_name,location,price,review,rating,link])
      # writer.writerow(['hotel_name','locality','price','review','rating','link'])

        print(hotel_name)
        print(location)
        print(price)
        print(review)
        print(rating)
        print(link)
        print('')


  else:
    print(f"connection failed!{response.status_code}")

# if using this script directly then below task will be executed

if __name__ == '__main__':

  url = input("please enter the url! : ")
  fn = input("please enter the file name! :")

  # calling the function
  web_scraper1(url,fn)
#https://www.booking.com/searchresults.html?ss=New%20Delhi&ssne=New%20Delhi&ssne_untouched=New%20Delhi&label=gen173nr-1FCAEoggI46AdIM1gEaGyIAQGYATG4ARfIAQzYAQHoAQH4AQKIAgGoAgO4AtSF670GwAIB0gIkOWQyOWM4ZmEtNDJiMy00YjBmLWFjNWYtMDAwNGY5ZjAzY2Mw2AIF4AIB&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-2106102&dest_type=city&checkin=2025-04-01&checkout=2025-04-02&group_adults=2&no_rooms=1&group_children=0