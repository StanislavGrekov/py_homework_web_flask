from __future__ import annotations
from flask import Flask, jsonify, request
from hashlib import md5
from flask.views import MethodView
from models import Session, Users, Advertisement
from schema import CreateUser, PatchUser, CreateAdvertisement, PatchAdvertisement
from typing import Type
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask("app")
app.config['JSON_AS_ASCII'] = False


def hashed_password(password):
    str_byte = password.encode()
    hashed_password = md5(str_byte).hexdigest()
    return hashed_password


def validate(json_data, model_class: Type[CreateUser] | Type[PatchUser] | Type[CreateAdvertisement] | Type[PatchAdvertisement], exclude_none: bool = True):
    try:
        model_item = model_class(**json_data)
        return model_item.dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise HttpError(400, er.errors())


class HttpError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


def get_user(user_id, session):
    user = session.get(Users, user_id)
    if user is None:
        raise HttpError(404, message='user not found')
    return user

###### Пользователи #####

class UserVeiw(MethodView):

    def get(self, user_id):
        with Session() as session:
            user = get_user(user_id, session)

            return jsonify({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'registration_date': user.registration_date.isoformat()
            })

    def post(self):

        json_data = validate(request.json, CreateUser)
        password = json_data['password']
        json_data['password'] = hashed_password(password)
        with Session() as session:
            new_user = Users(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'user alredy exists')
            return jsonify({'status': 'User added'})

    def patch(self, user_id):
        json_data = validate(request.json, PatchUser)
        if 'password' in json_data:
            json_data['password'] = hashed_password(json_data['password'])
        with Session() as session:
            user = get_user(user_id, session)
            for key, value in json_data.items():
                setattr(user, key, value)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'username is bisy')
            return jsonify({'id': user.last_name})

    def delete(self, user_id):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'Ok!'})

############ Объявления ############

class AdvertisementVeiw(MethodView):

    def post(self):
        json_data = validate(request.json, CreateAdvertisement)
        email = json_data['email']
        password = json_data['password']
        hash_password = hashed_password(password)

        with Session() as session:
            try:
                credentials = session.query(Users).filter(Users.email == email, Users.password == hash_password).first()
                adv = Advertisement(id_user=credentials.id, title=json_data['title'], description=json_data['description'])
                session.add(adv)
                session.commit()
            except AttributeError:
                raise HttpError(404, 'User not found or password incorrect')
            return jsonify({'status': 'Advertisement add!'})

    def get(self):
            with Session() as session:
                advertisement,my_list={},[]
                try:
                    for user in session.query(Users).all():
                        for adv in session.query(Advertisement).filter(Advertisement.id_user == user.id).all():
                            answer = f'Пользователь: {user.last_name}. Заголовок: {adv.title}, Описание: {adv.description}, Дата создания: {adv.created_fild}'
                            my_list.append(answer)
                    for i, val in enumerate(my_list, start=1):
                        advertisement[i] = val
                    return jsonify(advertisement)

                except AttributeError as er:
                    raise HttpError(404, 'User not found')

    def patch(self, adv_id):
        json_data = validate(request.json, CreateAdvertisement)
        email = json_data['email']
        password = json_data['password']
        hash_password = hashed_password(password)
        with Session() as session:
            title = json_data['title']
            description = json_data['description']
            try:
                credentials = session.query(Users).filter(Users.email == email, Users.password == hash_password).first()
                if credentials:
                    adv = session.query(Advertisement).filter(Advertisement.id == adv_id).update({"title" : title},
                                                                                           {"description": description}).one()
                    session.add(adv)
                    session.commit()
            except AttributeError:
                raise HttpError(404, 'User not found or password incorrect')
            return jsonify({'status': 'Advertisement changed!'})


    def delete(self, user_id):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'Ok!'})




############ Роуты #############

app.add_url_rule('/user/<int:user_id>',
                 view_func=UserVeiw.as_view('user_existed'),
                 methods=['GET', 'PATCH', 'DELETE', ])

app.add_url_rule('/user/',
                 view_func=UserVeiw.as_view('user_new'),
                 methods=['POST'])

app.add_url_rule('/Advertisement/', # Создание объявлений
                 view_func=AdvertisementVeiw.as_view('advertisement_new'),
                 methods=['POST'])

app.add_url_rule('/Advertisement/', # Получение всех объявлений
                 view_func=AdvertisementVeiw.as_view('advertisement_get'),
                 methods=['GET'])

app.add_url_rule('/Advertisement/<int:adv_id>',
                 view_func=AdvertisementVeiw.as_view('advertisement_patch_delete'),
                 methods=['PATCH', 'DELETE', ])

if __name__ == "__main__":
    app.run()
