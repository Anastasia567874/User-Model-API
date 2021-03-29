import flask
from . import db_session
from .users import User
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash
import datetime
import requests


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality',
                                    'address', 'about', 'email', 'hashed_password',
                                    'created_date', 'city_from'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_one_user(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'city_from',
                                         'address', 'about', 'email', 'hashed_password', 'created_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'position', 'speciality',
                  'address', 'about', 'email', 'hashed_password', 'city_from']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.id == request.json['id']:
            return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        about=request.json['about'],
        email=request.json['email'],
        hashed_password=generate_password_hash(request.json['hashed_password']),
        created_date=datetime.datetime.now(),
        city_from=request.json['city_from']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_user(users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(users_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def change_users(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'surname', 'age', 'position', 'speciality', 'city_from',
                  'address', 'about', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(users_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.about = request.json['about']
    user.email = request.json['email']
    user.hashed_password = generate_password_hash(request.json['hashed_password'])
    user.city_from = request.json['city_from']
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/users_show/<int:user_id>', methods=['GET'])
def get_city(user_id):
    global k
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return 'Пользователь не найден'
    f = 'none'
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={user.city_from}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={toponym_coodrinates[0]}%2C{toponym_coodrinates[1]}&size=600,450&z=9&l=sat"
        response = requests.get(map_request)
        f = f"static/img/city.jpg"
        with open(f, "wb") as file:
            file.write(response.content)
    return flask.render_template('city.html', name=f'{user.name} {user.surname}', city=user.city_from, f='/' + f)