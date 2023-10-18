import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

base_url="https://www.amazon.in/s"
search_query = "bags"  # Change this to your desired search query
page_number = 1  # Change this to the page number you want to scrape

product_urls=[]
product_name=[]
product_price=[]
product_rating=[]
product_reviews=[]

for page_number in range(1,21):
    params={
        "k":search_query,
        "page":page_number
        }
    
    response=requests.get(base_url,params=params)
    soup=BeautifulSoup(response.content,"html.parser")

    purls=soup.find_all("a",class_="a-link-normal")
    pname=soup.find_all("span",class_="a-text-normal")
    pprice=soup.find_all("span",class_="a-offscreen")
    prating=soup.find_all("span",class_="a-icon-alt")
    previews=soup.find_all("span",class_="a-size-base")

    for ur,name,price,rating,rev in zip(purls,pname,pprice,prating,previews):
        product_urls.append(ur.get('href'))
        product_name.append(name.text)
        product_price.append(price.text)
        product_rating.append(rating.text)
        product_reviews.append(rev.text)
    page_number+=1

#saving data in csv
data={"Product URL":product_urls,"Product Name":product_name,"Product Price":product_price,"Product Rating":product_rating,"Product Reviews":product_reviews}
df=pd.DataFrame(data)
df.to_csv("amazon.csv",index=False)
print(df)



                   
