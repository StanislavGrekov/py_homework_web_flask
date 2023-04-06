from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Users, Advertisement

app = Flask("app")


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
        json_data = request.json
        with Session() as session:
            new_user = Users(**json_data)
            session.add(new_user)
            session.commit()
            return jsonify({'status': 'OK'})


    def patch(self, user_id):
        pass

    def delete(self, user_id):
        pass


app.add_url_rule('/user/<int:user_id>',
                 view_func=UserVeiw.as_view('user_existed'),
                 methods=['GET', 'PATCH', 'DELETE',])

app.add_url_rule('/user/',
                 view_func=UserVeiw.as_view('user_new'),
                 methods=['POST'])


if __name__=="__main__":
    app.run()