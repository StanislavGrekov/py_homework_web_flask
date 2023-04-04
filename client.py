import requests
import uuid

response = requests.post('http://127.0.0.1:5000/hellow/',
                         json = {'key1': 'value1'},
                         params = {'k1':'v1'},
                         headers = {'token': str(uuid.uuid4())}
                         )

print(response.status_code)
answer = response.text
answ = answer[5:].replace('}','')
encoded = answ.encode('utf-8')

print(encoded.decode('utf-8'))