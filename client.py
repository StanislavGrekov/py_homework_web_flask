import requests
import uuid
from pprint import pprint

########### Регистрация пользователя #############

# response = requests.post('http://127.0.0.1:5000/user',
#                          json = {
#                             'first_name': 'Ivan',
#                             'last_name': 'Ivanov',
#                             'password':'password_net',
#                             'email': 'ivanov@yandex.ru',
#                         }
#                         )
#
# print(response.status_code)
# print(response.text)


######### Создание объявления ###################

# response = requests.post('http://127.0.0.1:5000/Advertisement',
#                          json = {
#                             'email': 'semen@yandex.ru',
#                             'password':'password_net',
#                             'title': 'Продам стол',
#                             'description':'хороший стол продаю',
#                         }
#                         )
#
# print(response.status_code)
# print(response.text)


####### Получение всех объявлений ###################

# response = requests.get('http://127.0.0.1:5000/Advertisement')
#
# print(response.status_code)
# print(response.text)

######### Изменить объявления ###################

response = requests.patch('http://127.0.0.1:5000/Advertisement/4',
                         json = {
                            'email': 'semen@yandex.ru',
                            'password':'password_net',
                            'title': 'Объявление убрал',
                            'description': 'Стол продал',
                        }
                        )

print(response.status_code)
print(response.text)







# response = requests.patch('http://127.0.0.1:5000/user/1',
#                          json = {
#                          'password':'password',}
#                          )
#
# print(response.status_code)
# print(response.text)
#

# response = requests.get('http://127.0.0.1:5000/user/3')
#
# print(response.status_code)
# print(response.text)



# response = requests.delete('http://127.0.0.1:5000/user/5')
#
# print(response.status_code)
# print(response.text)