import requests
import uuid

# response = requests.post('http://127.0.0.1:5000/user/',
#                          json = {'email':'stas.ik1987@yandex.ru', 'password':'njhkhhhjkhkjh', 'first_name':'GREKOV', 'last_name':'Stanislav'}
#                          )
#
# print(response.status_code)
# print(response.text)

response = requests.get('http://127.0.0.1:5000/user/2')

print(response.status_code)
print(response.text)