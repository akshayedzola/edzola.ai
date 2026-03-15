import requests

url = "https://forms.zohopublic.com/zohodocs1155/form/edzolaai/formperma/v9WjnW3jGyXO5Mj8dXD3mzmhbJn16vCLscXlxB02QHY/submit"

data = {
    "Email": "test@ed.com"
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
