import requests

product_ids = []

products_url = "https://catering.mukhsin.space/api/v1/products/"
warehouses_url = "https://catering.mukhsin.space/api/v1/warehouses/"

next_exists = True

while next_exists:
    products = requests.get(url=products_url).json()
    if products["next"] == None:
        next_exists = False
    products_url = products["next"]

    for i in products["results"]:
        product_ids.append(i["id"])

for product_id in product_ids:
    response = requests.post(url=warehouses_url, data={"arrived_amount": 300, "gross_price": 300, "product": product_id})
    print(response.status_code)
