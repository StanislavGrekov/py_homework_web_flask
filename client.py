import requests
import uuid

response = requests.patch('http://127.0.0.1:5000/user/1',
                         json = {
                         'password':'password',}
                         )

print(response.status_code)
print(response.text)

# response = requests.get('http://127.0.0.1:5000/user/3')
#
# print(response.status_code)
# print(response.text)



# response = requests.delete('http://127.0.0.1:5000/user/5')
#
# print(response.status_code)
# print(response.text)