from requests import get, post


print(post('http://localhost:5000/api/users',
           json={'id': 1, 'name': 'Mark', 'surname': 'Watny', 'age': 23, 'position': 'eng',
                 'speciality': 'spec', 'address': 'module_1', 'about': 'None', 'email': 'mark@gmail.com',
                 'hashed_password': 'poi567voi', 'city_from': 'Moscow'}).json())
print(post('http://localhost:5000/api/users',
           json={'id': 2, 'name': 'Andy', 'surname': 'Weir', 'age': 27, 'position': 'eng',
                 'speciality': 'spec', 'address': 'module_2', 'about': 'None', 'email': 'andy@gmail.com',
                 'hashed_password': 'qwerty234', 'city_from': 'Wellington'}).json())
print(get('http://localhost:5000/api/users').json())