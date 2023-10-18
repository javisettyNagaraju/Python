
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.amazon.in/s"
search_query = "bags"
data = []

for page in range(1, 21):  # Scrape 20 pages
    params = {
        "k": search_query,
        "crid": "2M096C61O4MLT",
        "qid": "1653308124",
        "sprefix": "ba",
        "ref": f"sr_pg_{page}",
    }
    
response = requests.get(base_url,params=params)
soup = BeautifulSoup(response.text, 'html.parser')
products = soup.find_all("div", {"data-component-type": "s-search-result"})

for product in products:
    product_url = "https://www.amazon.in" + product.find("a", {"class": "a-link-normal"})['href']
    product_name = product.find("span", {"class": "a-text-normal"}).get_text()
    product_price = product.find("span", {"class": "a-offscreen"}).get_text()
    rating = product.find("span", {"class": "a-icon-alt"})
    rating = rating.get_text() if rating else "N/A"
    num_reviews = product.find("span", {"class": "a-size-base"}).get_text()

    data.append([product_url, product_name, product_price, rating, num_reviews])

# Convert data to a DataFrame and export to CSV
    
df = pd.DataFrame(data, columns=["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])
df.to_csv("amazon_product_listings.csv", index=False)
print(df)


'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the CSV file with product URLs
df = pd.read_csv("amazon_product_listings.csv")

additional_data = []

for url in df["Product URL"]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract additional information
    description = soup.find("div", {"id": "productDescription"}).get_text() if soup.find("div", {"id": "productDescription"}) else "N/A"
    asin = soup.find("th", text="ASIN").find_next("td").get_text() if soup.find("th", text="ASIN") else "N/A"
    product_description = soup.find("span", {"class": "a-text-ellipsis"}).get_text() if soup.find("span", {"class": "a-text-ellipsis"}) else "N/A"
    manufacturer = soup.find("th", text="Manufacturer").find_next("td").get_text() if soup.find("th", text="Manufacturer") else "N/A"

    additional_data.append([description, asin, product_description, manufacturer])

# Add the additional data to the existing DataFrame
df["Description"] = [entry[0] for entry in additional_data]
df["ASIN"] = [entry[1] for entry in additional_data]
df["Product Description"] = [entry[2] for entry in additional_data]
df["Manufacturer"] = [entry[3] for entry in additional_data]

# Export the updated DataFrame to a CSV file
df.to_csv("amazon_product_info.csv", index=False)
print(additional_data)
'''

