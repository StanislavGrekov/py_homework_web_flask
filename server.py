from flask import Flask, jsonify, request


app = Flask("app")

def hellow():
    json_data = request.json
    headers = request.headers
    qs = request.args
    print(json_data,headers,qs)

    return jsonify({'answer': 'Ok!'})

app.add_url_rule('/hellow/', view_func=hellow, methods=['POST', ])


if __name__=="__main__":
    app.run()