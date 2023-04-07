from flask import Flask, jsonify, request
from hashlib import md5
from flask.views import MethodView
from models import Session, Users, Advertisement
from schema import CreateUser, PatchUser
from typing import Type
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


app = Flask("app")

def hashed_password(password):
    str_byte = password.encode()
    hashed_password = md5(str_byte).hexdigest()
    return hashed_password

def validate(json_data, model_class: Type[CreateUser] | Type[PatchUser], exclude_none: bool = True):
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

    response.status_code=error.status_code

    return response

def get_user(user_id, session):
    user = session.get(Users, user_id)
    if user is None:
        raise HttpError(404, message='user not found')
    return user

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
            return jsonify({'status': 'OK'})

    def patch(self, user_id):
        json_data = validate(request.json, PatchUser)
        if 'password' in json_data:
            json_data['password'] = hashed_password(json_data['password'])
        with Session() as session:
            user = get_user(user_id, session)
            for key, value in json_data.items():
                setattr (user, key, value)
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
            return  jsonify({'status':'Ok!'})



app.add_url_rule('/user/<int:user_id>',
                 view_func=UserVeiw.as_view('user_existed'),
                 methods=['GET', 'PATCH', 'DELETE',])

app.add_url_rule('/user/',
                 view_func=UserVeiw.as_view('user_new'),
                 methods=['POST'])


if __name__=="__main__":
    app.run()