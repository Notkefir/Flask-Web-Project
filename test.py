from requests import get, post, delete

print('Proposals:')
print(get('http://localhost:8080/api/v2/proposals').json())

print(post('http://localhost:8080/api/v2/proposals', json={'title': 'Writing',
                                                           'phone_number': '444545454545',
                                                           'coast': 1005.09,
                                                           'user_id': 1}))

print(get('http://localhost:8080/api/v2/proposals/3').json())

print(get('http://localhost:8080/api/v2/proposals/999').json())

print(delete('http://localhost:8080/api/v2/proposals/3').json())

print(delete('http://localhost:8080/api/v2/proposals/999').json())

print('-----------------')

print('Users:')
print(get('http://localhost:8080/api/v2/users').json())

print(post('http://localhost:8080/api/v2/users', json={'name': 'da',
                                                       'surname': 'net',
                                                       'email': 'email@ya.ru',
                                                       'specialization': 'Репетитор',
                                                       'hashed_password': '123',
                                                       'age': 12,
                                                       'about': 'dddffdf',
                                                       'address': 'qqqq'
                                                       }))

print(get('http://localhost:8080/api/v2/users/2').json())

print(get('http://localhost:8080/api/v2/users/999').json())

print(delete('http://localhost:8080/api/v2/users/2').json())

print(delete('http://localhost:8080/api/v2/users/999').json())
