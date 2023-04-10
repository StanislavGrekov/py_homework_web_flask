import requests


########## Регистрация пользователя #############

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


######## Создание объявления ###################

# response = requests.post('http://127.0.0.1:5000/Advertisement',
#                          json = {
#                             'email': 'ivanov@yandex.ru',
#                             'password':'password_net',
#                             'title': 'Продам стол',
#                             'description':'хороший стол продаю',
#                         }
#                         )
#
# print(response.status_code)
# print(response.text)
# #

###### Получение всех объявлений ###################
#
# response = requests.get('http://127.0.0.1:5000/Advertisement')
#
# print(response.status_code)
# print(response.text)


######### Изменить объявления ###################

# response = requests.patch('http://127.0.0.1:5000/Advertisement/8',
#                          json = {
#                             'email': 'ivanov@yandex.ru',
#                             'password':'password_net',
#                             'title': 'Плохое слово1',
#                             'description': 'Стол продан',
#                         }
#                         )
#
# print(response.status_code)
# print(response.text)

#
######### Удалить объявления ###################

# response = requests.delete('http://127.0.0.1:5000/Advertisement/7',
#                          json = {
#                             'email': 'ivanov@yandex.ru',
#                             'password':'password_net',
#                         }
#                         )
#
# print(response.status_code)
# print(response.text)




