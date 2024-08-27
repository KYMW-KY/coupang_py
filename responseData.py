import requests
import json

class response:
    def get_products_by_category(self, category):
        url = f'http://localhost:8080/product/get'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Request failed with status code:", response.status_code)